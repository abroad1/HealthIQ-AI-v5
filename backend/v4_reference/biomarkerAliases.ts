/**
 * Biomarker Aliases Service
 * 
 * Loads and caches biomarker aliases from the centralized API.
 * Provides client-side resolution and validation.
 */

export interface BiomarkerAliases {
  canonical_to_aliases: Record<string, string[]>;
  alias_to_canonical: Record<string, string>;
  all_canonical_ids: string[];
  metadata: {
    last_updated: string;
    total_canonical: number;
    total_aliases: number;
    performance_metrics?: {
      cache_hits: number;
      cache_misses: number;
      total_requests: number;
      hit_rate_percent: number;
      cache_size: number;
    };
  };
}

class BiomarkerAliasesService {
  private aliases: BiomarkerAliases | null = null;
  private loading = false;
  private error: string | null = null;
  private lastFetch: number = 0;
  private readonly CACHE_DURATION = 5 * 60 * 1000; // 5 minutes

  /**
   * Load biomarker aliases from the API
   */
  async loadAliases(): Promise<BiomarkerAliases> {
    // Return cached data if still valid
    if (this.aliases && Date.now() - this.lastFetch < this.CACHE_DURATION) {
      return this.aliases;
    }

    // Prevent multiple simultaneous requests
    if (this.loading) {
      while (this.loading) {
        await new Promise(resolve => setTimeout(resolve, 100));
      }
      return this.aliases!;
    }

    this.loading = true;
    this.error = null;

    try {
      const response = await fetch('/api/v1/biomarker-aliases');
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      this.aliases = await response.json();
      this.lastFetch = Date.now();
      
      console.log(`✅ Loaded ${this.aliases.metadata.total_canonical} canonical biomarkers with ${this.aliases.metadata.total_aliases} aliases`);
      
      return this.aliases;
    } catch (error) {
      this.error = error instanceof Error ? error.message : 'Unknown error';
      console.error('❌ Failed to load biomarker aliases:', error);
      throw error;
    } finally {
      this.loading = false;
    }
  }

  /**
   * Resolve a biomarker alias to its canonical ID
   */
  resolveToCanonical(alias: string): string {
    if (!this.aliases) {
      console.warn('Biomarker aliases not loaded, returning original alias');
      return alias;
    }

    const canonical = this.aliases.alias_to_canonical[alias];
    return canonical || alias;
  }

  /**
   * Get all aliases for a canonical ID
   */
  getAliasesForCanonical(canonicalId: string): string[] {
    if (!this.aliases) {
      return [];
    }

    return this.aliases.canonical_to_aliases[canonicalId] || [];
  }

  /**
   * Check if a name is a canonical ID
   */
  isCanonicalId(name: string): boolean {
    if (!this.aliases) {
      return false;
    }

    return this.aliases.all_canonical_ids.includes(name);
  }

  /**
   * Validate a panel of biomarkers
   */
  validatePanel(panel: Record<string, any>): {
    unknown_aliases: string[];
    resolved_mappings: Record<string, string>;
  } {
    if (!this.aliases) {
      return {
        unknown_aliases: Object.keys(panel),
        resolved_mappings: {}
      };
    }

    const unknown_aliases: string[] = [];
    const resolved_mappings: Record<string, string> = {};

    for (const alias of Object.keys(panel)) {
      const canonical = this.resolveToCanonical(alias);
      resolved_mappings[alias] = canonical;

      if (canonical === alias && !this.isCanonicalId(alias)) {
        unknown_aliases.push(alias);
      }
    }

    return {
      unknown_aliases,
      resolved_mappings
    };
  }

  /**
   * Get the current aliases data
   */
  getAliases(): BiomarkerAliases | null {
    return this.aliases;
  }

  /**
   * Get loading state
   */
  isLoading(): boolean {
    return this.loading;
  }

  /**
   * Get error state
   */
  getError(): string | null {
    return this.error;
  }

  /**
   * Clear cache and force reload
   */
  clearCache(): void {
    this.aliases = null;
    this.lastFetch = 0;
    this.error = null;
  }
}

// Export singleton instance
export const biomarkerAliasesService = new BiomarkerAliasesService();

// Export convenience functions
export const resolveToCanonical = (alias: string) => biomarkerAliasesService.resolveToCanonical(alias);
export const isCanonicalId = (name: string) => biomarkerAliasesService.isCanonicalId(name);
export const validatePanel = (panel: Record<string, any>) => biomarkerAliasesService.validatePanel(panel); 
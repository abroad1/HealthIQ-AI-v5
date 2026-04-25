'use client';

import React from 'react';
import { pingHealth, startAnalysis, getAnalysisResult } from '../lib/api';
import { useAnalysisStore } from '../state/analysisStore';
import { useClusterStore } from '../state/clusterStore';
import { useUIStore } from '../state/uiStore';

/**
 * Dev-only: uses the same R-2A contract as the app (sync POST /start, then GET /result) — no SSE.
 */
export default function DevApiProbe() {
  const [status, setStatus] = React.useState<string>('idle');
  const [logs, setLogs] = React.useState<string[]>([]);
  const [analysisId, setAnalysisId] = React.useState<string | null>(null);

  const analysisStore = useAnalysisStore();
  const clusterStore = useClusterStore();
  const uiStore = useUIStore();

  function log(line: string) {
    setLogs((prev) => [new Date().toLocaleTimeString() + ' — ' + line, ...prev].slice(0, 200));
  }

  async function handlePing() {
    setStatus('pinging');
    try {
      const data = await pingHealth();
      log('health: ' + JSON.stringify(data));
      setStatus('ok');
    } catch (e: unknown) {
      log('health ERROR: ' + (e instanceof Error ? e.message : String(e)));
      setStatus('error');
    }
  }

  async function handleStartAnalysis() {
    try {
      const payload = {
        biomarkers: {
          cholesterol: { value: 4.9, unit: 'mmol/L' },
          blood_sugar: { value: 4.8, unit: 'mmol/L' },
        },
        user: {
          chronological_age: 58,
          sex: 'male' as const,
          weight_kg: 80,
          height_cm: 178,
        },
      };

      log('Starting analysis with payload: ' + JSON.stringify(payload));

      await analysisStore.startAnalysis(payload);

      uiStore.addToast({
        type: 'info',
        title: 'Analysis started',
        message: 'POST /api/analysis/start completed; use Fetch result to load GET /result.',
        duration: 3000,
        position: 'top-right',
      });

      const currentAnalysis = analysisStore.currentAnalysis;
      if (currentAnalysis) {
        setAnalysisId(currentAnalysis.analysis_id);
        log('Analysis id: ' + currentAnalysis.analysis_id + ' (phase: ' + analysisStore.currentPhase + ')');
      }
    } catch (e: unknown) {
      log('startAnalysis ERROR: ' + (e instanceof Error ? e.message : String(e)));
      const id = useAnalysisStore.getState().currentAnalysisId;
      if (id) {
        analysisStore.failAnalysis(id, {
          message: e instanceof Error ? e.message : String(e),
          code: 'ANALYSIS_START_ERROR',
        });
      }
      uiStore.addToast({
        type: 'error',
        title: 'Analysis failed',
        message: 'Failed to start biomarker analysis',
        duration: 5000,
        position: 'top-right',
      });
    }
  }

  async function handleFetchResult() {
    if (!analysisId) {
      log('No analysisId yet');
      return;
    }
    try {
      const data = await getAnalysisResult(analysisId);
      log('result: ' + JSON.stringify(data).slice(0, 2000));
    } catch (e: unknown) {
      log('getAnalysisResult ERROR: ' + (e instanceof Error ? e.message : String(e)));
    }
  }

  return (
    <div
      style={{ position: 'fixed', right: 16, bottom: 16, zIndex: 9999, maxWidth: 500 }}
      className="rounded-xl border p-3 shadow bg-white/90 backdrop-blur"
    >
      <div className="flex items-center justify-between gap-2 mb-2">
        <strong>Dev API Probe + Store State</strong>
        <span style={{ fontSize: 12, opacity: 0.7 }}>status: {status}</span>
      </div>

      <div className="mb-3 p-2 bg-gray-50 rounded text-xs">
        <div className="font-semibold mb-1">Store States:</div>
        <div>
          <strong>Analysis:</strong> {analysisStore.currentPhase} ({analysisStore.progress}%)
        </div>
        <div>
          <strong>Clusters:</strong> {clusterStore.clusters.length} loaded
        </div>
        <div>
          <strong>UI:</strong> {uiStore.toasts.length} toasts, {uiStore.notifications.length} notifications
        </div>
        <div>
          <strong>Theme:</strong> {uiStore.actualTheme}
        </div>
      </div>

      <div className="flex gap-2 mb-2 flex-wrap">
        <button
          onClick={handlePing}
          className="px-3 py-1 rounded bg-black text-white text-xs"
          type="button"
        >
          Ping API
        </button>
        <button
          onClick={handleStartAnalysis}
          className="px-3 py-1 rounded bg-green-600 text-white text-xs"
          type="button"
        >
          Start analysis
        </button>
        <button
          onClick={handleFetchResult}
          className="px-3 py-1 rounded bg-purple-600 text-white text-xs"
          type="button"
          disabled={!analysisId}
        >
          Fetch result
        </button>
        <button
          onClick={() => uiStore.toggleTheme()}
          className="px-3 py-1 rounded bg-indigo-600 text-white text-xs"
          type="button"
        >
          Toggle theme
        </button>
        <button
          onClick={() => clusterStore.loadClusters('demo')}
          className="px-3 py-1 rounded bg-orange-600 text-white text-xs"
          type="button"
        >
          Load clusters
        </button>
      </div>

      <div
        style={{
          maxHeight: 200,
          overflow: 'auto',
          fontFamily: 'ui-monospace, SFMono-Regular, Menlo, monospace',
          fontSize: 12,
          lineHeight: 1.4,
        }}
      >
        {logs.length === 0 ? <div style={{ opacity: 0.6 }}>No logs yet…</div> : logs.map((l, i) => <div key={i}>{l}</div>)}
      </div>

      <div className="text-[11px] opacity-60 mt-1.5">
        R-2A: no SSE. Using API_BASE: <code>{process.env.NEXT_PUBLIC_API_BASE ?? 'http://127.0.0.1:8000'}</code>
      </div>
    </div>
  );
}

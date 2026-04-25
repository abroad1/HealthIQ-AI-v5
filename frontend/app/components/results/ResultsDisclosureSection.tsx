'use client';

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { ChevronDown, ChevronRight } from 'lucide-react';
import { useId, useState, type ReactNode } from 'react';

export interface ResultsDisclosureSectionProps {
  title: string;
  description?: string;
  defaultOpen?: boolean;
  className?: string;
  'data-testid'?: string;
  children: ReactNode;
  onOpenChange?: (open: boolean) => void;
}

export function ResultsDisclosureSection({
  title,
  description,
  defaultOpen = false,
  className = '',
  'data-testid': dataTestId,
  children,
  onOpenChange,
}: ResultsDisclosureSectionProps) {
  const [open, setOpen] = useState(defaultOpen);
  const regionId = useId();

  const toggle = () => {
    setOpen((o) => {
      const n = !o;
      onOpenChange?.(n);
      return n;
    });
  };

  return (
    <section className={className} data-testid={dataTestId}>
      <Card className="border-slate-200 shadow-sm">
        <CardHeader className="pb-2">
          <div className="flex flex-wrap items-start justify-between gap-2">
            <div>
              <CardTitle className="text-lg">{title}</CardTitle>
              {description ? <CardDescription className="mt-1 max-w-prose">{description}</CardDescription> : null}
            </div>
            <Button
              type="button"
              variant="outline"
              size="sm"
              onClick={toggle}
              aria-expanded={open}
              aria-controls={regionId}
            >
              {open ? (
                <>
                  <ChevronDown className="h-4 w-4 mr-2" />
                  Hide
                </>
              ) : (
                <>
                  <ChevronRight className="h-4 w-4 mr-2" />
                  Show
                </>
              )}
            </Button>
          </div>
        </CardHeader>
        {open ? (
          <CardContent id={regionId} className="pt-0 space-y-6 border-t border-slate-100">
            {children}
          </CardContent>
        ) : null}
      </Card>
    </section>
  );
}

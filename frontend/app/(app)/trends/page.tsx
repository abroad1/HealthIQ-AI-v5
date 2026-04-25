'use client';

import Link from 'next/link';
import { ArrowDown, ArrowRight, ArrowUp, Loader2, Minus, TrendingUp, Upload } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { useTrendData } from '@/hooks/useTrendData';
import type { TrendArrow } from '@/lib/trendComparison';

function TrendArrowIcon({ arrow }: { arrow: TrendArrow }) {
  const common = 'h-4 w-4 shrink-0';
  switch (arrow) {
    case 'up':
      return <ArrowUp className={common} aria-hidden />;
    case 'down':
      return <ArrowDown className={common} aria-hidden />;
    case 'flat':
      return <Minus className={common} aria-hidden />;
    default:
      return <ArrowRight className={`${common} text-muted-foreground`} aria-hidden />;
  }
}

function arrowLabel(arrow: TrendArrow): string {
  switch (arrow) {
    case 'up':
      return 'Increased since last test';
    case 'down':
      return 'Decreased since last test';
    case 'flat':
      return 'Unchanged since last test';
    default:
      return 'No comparison';
  }
}

export default function TrendsPage() {
  const trend = useTrendData(true);

  return (
    <div className="container max-w-5xl py-8 space-y-8">
      <div className="flex flex-col gap-3 md:flex-row md:items-end md:justify-between">
        <div>
          <div className="flex items-center gap-2 text-indigo-700 mb-1">
            <TrendingUp className="h-6 w-6" aria-hidden />
            <span className="text-sm font-semibold uppercase tracking-wide">Trends</span>
          </div>
          <h1 className="text-3xl font-bold tracking-tight">Marker changes over time</h1>
          <p className="text-muted-foreground mt-2 max-w-2xl">
            Compare your most recent blood test to the one before it. Sorted by the largest absolute change
            first.
          </p>
        </div>
        <Button asChild variant="outline" size="sm">
          <Link href="/dashboard">Back to dashboard</Link>
        </Button>
      </div>

      {trend.status === 'loading' ? (
        <div className="flex items-center gap-2 text-muted-foreground py-12">
          <Loader2 className="h-5 w-5 animate-spin" aria-hidden />
          <span>Loading your analyses…</span>
        </div>
      ) : null}

      {trend.status === 'error' ? (
        <Alert variant="destructive">
          <AlertDescription>{trend.message}</AlertDescription>
        </Alert>
      ) : null}

      {trend.status === 'insufficient' ? (
        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Trends need another test</CardTitle>
            <CardDescription>
              {trend.completedCount === 0
                ? 'Complete an analysis first, then upload another blood test to see how your markers move.'
                : 'Upload another blood test to see your trends.'}
            </CardDescription>
          </CardHeader>
          <CardContent className="flex flex-wrap gap-3">
            <Button asChild>
              <Link href="/upload">
                <Upload className="h-4 w-4 mr-2" aria-hidden />
                Go to upload
              </Link>
            </Button>
            <Button asChild variant="secondary">
              <Link href="/reports">View reports</Link>
            </Button>
          </CardContent>
        </Card>
      ) : null}

      {trend.status === 'ready' ? (
        <div className="space-y-4">
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-base">Comparison</CardTitle>
              <CardDescription>
                Latest: {new Date(trend.recentItem.created_at).toLocaleString()} · Previous:{' '}
                {new Date(trend.previousItem.created_at).toLocaleString()}
              </CardDescription>
            </CardHeader>
            <CardContent className="overflow-x-auto pt-0">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Biomarker</TableHead>
                    <TableHead className="text-right">Most recent</TableHead>
                    <TableHead className="text-right">Previous</TableHead>
                    <TableHead className="text-right">Change</TableHead>
                    <TableHead className="w-[72px] text-center">Trend</TableHead>
                    <TableHead>Range status (latest)</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {trend.rows.length === 0 ? (
                    <TableRow>
                      <TableCell colSpan={6} className="text-muted-foreground text-center py-8">
                        No biomarker rows in these results.
                      </TableCell>
                    </TableRow>
                  ) : (
                    trend.rows.map((row) => (
                      <TableRow key={row.biomarkerName}>
                        <TableCell className="font-medium">{row.biomarkerName}</TableCell>
                        <TableCell className="text-right tabular-nums">{row.recentDisplay}</TableCell>
                        <TableCell className="text-right tabular-nums text-muted-foreground">
                          {row.previousDisplay}
                        </TableCell>
                        <TableCell className="text-right tabular-nums">{row.deltaDisplay}</TableCell>
                        <TableCell className="text-center">
                          <span title={arrowLabel(row.arrow)} className="inline-flex justify-center">
                            <TrendArrowIcon arrow={row.arrow} />
                          </span>
                        </TableCell>
                        <TableCell className="text-muted-foreground">{row.rangeStatusLabel}</TableCell>
                      </TableRow>
                    ))
                  )}
                </TableBody>
              </Table>
            </CardContent>
          </Card>
          <p className="text-xs text-muted-foreground">
            Change values are simple differences between numeric results (most recent minus previous). They are
            not clinical interpretations.
          </p>
        </div>
      ) : null}
    </div>
  );
}

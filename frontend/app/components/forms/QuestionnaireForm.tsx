'use client';

import React, { useState, useEffect, useCallback, useMemo, useRef } from 'react';
import { DM_Serif_Display } from 'next/font/google';
import { Button } from '../ui/button';
import { Card, CardContent } from '../ui/card';
import { Input } from '../ui/input';
import { Label } from '../ui/label';
import { Slider } from '../ui/slider';
import { Textarea } from '../ui/textarea';
import { Alert, AlertDescription } from '../ui/alert';
import { Loader2, AlertCircle, Check, ChevronRight } from 'lucide-react';
import {
  fetchQuestionnaireSchema,
  type QuestionnaireQuestion,
} from '@/lib/questionnaireSchema';
import { cn } from '@/lib/utils';

const dmSerif = DM_Serif_Display({ weight: '400', subsets: ['latin'], display: 'swap' });

/** Question card shell — diagnostic panel, not floating shadcn default */
const questionCardClass =
  'border border-border bg-card shadow-none hover:border-border/80 hover:shadow-sm transition-all duration-200';

function isRecord(v: unknown): v is Record<string, unknown> {
  return v !== null && typeof v === 'object' && !Array.isArray(v);
}

function asString(v: unknown): string {
  if (v === null || v === undefined) return '';
  if (typeof v === 'string') return v;
  if (typeof v === 'number' || typeof v === 'boolean') return String(v);
  return '';
}

function isQuestionVisible(question: QuestionnaireQuestion, responses: Record<string, unknown>): boolean {
  const cd = question.conditionalDisplay;
  if (!cd) return true;
  const depVal = responses[cd.dependsOn];
  return cd.showWhen.includes(String(depVal));
}

const SECTION_KEYS = [
  'demographics',
  'medical_history',
  'symptoms',
  'lifestyle',
  'physical_assessment',
  'cognitive_assessment',
  'family_history',
] as const;

type SectionKey = (typeof SECTION_KEYS)[number];

const SECTION_META: Record<
  SectionKey,
  { label: string; icon: string; estimate: string }
> = {
  demographics: { label: 'About you', icon: '👤', estimate: '~2 min' },
  medical_history: { label: 'Health history', icon: '🏥', estimate: '~3 min' },
  symptoms: { label: 'How you feel', icon: '💬', estimate: '~1 min' },
  lifestyle: { label: 'Daily habits', icon: '🌿', estimate: '~3 min' },
  physical_assessment: { label: 'Physical ability', icon: '💪', estimate: '~2 min' },
  cognitive_assessment: { label: 'Mental sharpness', icon: '🧠', estimate: '~1 min' },
  family_history: { label: 'Family story', icon: '🧬', estimate: '~1 min' },
};

interface QuestionnaireFormProps {
  onSubmit: (responses: Record<string, unknown>) => void;
  onCancel?: () => void;
  initialData?: Record<string, unknown>;
  isLoading?: boolean;
}

function useOnClickOutside(ref: React.RefObject<HTMLElement | null>, handler: () => void, enabled: boolean) {
  useEffect(() => {
    if (!enabled) return;
    function listener(event: MouseEvent) {
      const el = ref.current;
      if (!el || el.contains(event.target as Node)) return;
      handler();
    }
    document.addEventListener('mousedown', listener);
    return () => document.removeEventListener('mousedown', listener);
  }, [ref, handler, enabled]);
}

function SearchableSelect(props: {
  id: string;
  options: string[];
  value: string;
  onChange: (v: string) => void;
  placeholder?: string;
  error?: boolean;
  disabled?: boolean;
}) {
  const { id, options, value, onChange, placeholder = 'Search or choose…', error, disabled } = props;
  const [open, setOpen] = useState(false);
  const [filter, setFilter] = useState('');
  const rootRef = useRef<HTMLDivElement>(null);

  const filtered = useMemo(() => {
    const q = filter.trim().toLowerCase();
    if (!q) return options;
    return options.filter((o) => o.toLowerCase().includes(q));
  }, [options, filter]);

  useOnClickOutside(rootRef, () => setOpen(false), open);

  return (
    <div ref={rootRef} className="relative">
      <button
        id={id}
        type="button"
        disabled={disabled}
        aria-expanded={open}
        aria-haspopup="listbox"
        onClick={() => !disabled && setOpen((o) => !o)}
        className={cn(
          'flex h-11 w-full items-center justify-between rounded-lg border border-border bg-background px-3 text-left text-sm transition-all duration-150 hover:border-primary/50 hover:bg-primary/5',
          error ? 'border-destructive' : 'border-input',
          disabled && 'cursor-not-allowed opacity-60'
        )}
      >
        <span className={cn(!value && 'text-muted-foreground')}>{value || placeholder}</span>
        <ChevronRight className={cn('h-4 w-4 shrink-0 rotate-90 text-muted-foreground transition-transform', open && 'rotate-[270deg]')} />
      </button>
      {open && (
        <div className="absolute left-0 right-0 top-full z-50 mt-1 rounded-lg border bg-popover p-2 shadow-lg">
          <Input
            value={filter}
            onChange={(e) => setFilter(e.target.value)}
            placeholder="Type to filter…"
            className="mb-2 h-9"
            autoFocus
          />
          <div role="listbox" className="max-h-52 overflow-y-auto space-y-0.5">
            {filtered.map((opt) => (
              <button
                key={opt}
                type="button"
                role="option"
                aria-selected={opt === value}
                className={cn(
                  'flex w-full items-center rounded-md px-2 py-2 text-left text-sm transition-colors hover:bg-accent',
                  opt === value && 'bg-primary text-primary-foreground'
                )}
                onClick={() => {
                  onChange(opt);
                  setOpen(false);
                  setFilter('');
                }}
              >
                {opt === value && <Check className="mr-2 h-4 w-4 shrink-0" />}
                <span className={cn(opt !== value && 'pl-6')}>{opt}</span>
              </button>
            ))}
            {filtered.length === 0 && (
              <p className="px-2 py-3 text-center text-xs text-muted-foreground">No matches</p>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

export default function QuestionnaireForm({
  onSubmit,
  onCancel,
  initialData = {},
  isLoading = false,
}: QuestionnaireFormProps) {
  const [questions, setQuestions] = useState<QuestionnaireQuestion[]>([]);
  const [responses, setResponses] = useState<Record<string, unknown>>(initialData);
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [loadingQuestions, setLoadingQuestions] = useState(true);
  const [schemaLoadError, setSchemaLoadError] = useState<string | null>(null);

  const [flowPhase, setFlowPhase] = useState<'intent' | 'sections'>('intent');
  const [activeSectionIdx, setActiveSectionIdx] = useState(0);

  const busy = isSubmitting || isLoading;

  const loadQuestions = useCallback(async () => {
    setSchemaLoadError(null);
    setLoadingQuestions(true);
    try {
      const schema = await fetchQuestionnaireSchema();
      setQuestions(schema);
    } catch (error) {
      const message =
        error instanceof Error ? error.message : 'Failed to load questionnaire schema';
      console.error('Questionnaire schema load failed:', error);
      setSchemaLoadError(message);
      setQuestions([]);
    } finally {
      setLoadingQuestions(false);
    }
  }, []);

  useEffect(() => {
    loadQuestions();
  }, [loadQuestions]);

  /** Dev/test only: `?autofill=true` loads sample answers from `@/lib/mock/questionnaire` (not the question list). */
  useEffect(() => {
    if (typeof window !== 'undefined' && window.location.search.includes('autofill=true')) {
      void import('@/lib/mock/questionnaire').then((m) => {
        setResponses(m.default);
        console.log('🧪 Questionnaire responses auto-filled (mock answers only)');
      });
    }
  }, []);

  const sectionsOrdered = useMemo(() => {
    return SECTION_KEYS.map((key) => ({
      key,
      meta: SECTION_META[key],
      questions: questions.filter((q) => q.section === key),
    }));
  }, [questions]);

  const stripSectionErrors = useCallback((sectionKey: SectionKey, prev: Record<string, string>) => {
    const sectionQs = questions.filter((q) => q.section === sectionKey);
    const next = { ...prev };
    for (const q of sectionQs) {
      delete next[q.id];
    }
    return next;
  }, [questions]);

  const validateQuestion = useCallback((question: QuestionnaireQuestion): string | undefined => {
    if (!isQuestionVisible(question, responses)) return undefined;

    const value = responses[question.id];

    const reqHint = question.required ? 'This field is required' : undefined;

    if (question.required) {
      if (question.type === 'checkbox') {
        if (!Array.isArray(value) || value.length === 0) {
          return reqHint;
        }
      } else if (question.type === 'group') {
        const obj = isRecord(value) ? value : {};
        for (const field of question.fields ?? []) {
          const fv = obj[field.label];
          if (
            fv === undefined ||
            fv === '' ||
            (field.type === 'number' &&
              (fv === null || (typeof fv === 'number' && Number.isNaN(fv)) || fv === ''))
          ) {
            return `${field.label} is required`;
          }
        }
      } else if (
        value === undefined ||
        value === null ||
        value === '' ||
        (typeof value === 'number' && Number.isNaN(value))
      ) {
        return reqHint;
      }
    }

    if (question.type === 'email' && value) {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(asString(value))) {
        return 'Please enter a valid email address';
      }
    }

    if (question.type === 'phone' && value) {
      const phoneRegex = /^[\d\s()+-]{6,}$/;
      if (!phoneRegex.test(asString(value))) {
        return 'Please enter a valid phone number';
      }
    }

    if (question.type === 'number' && value !== undefined && value !== null && value !== '') {
      if (Number.isNaN(parseFloat(asString(value)))) {
        return 'Please enter a valid number';
      }
    }

    return undefined;
  }, [responses]);

  const validateActiveSection = useCallback((): boolean => {
    const key = SECTION_KEYS[activeSectionIdx];
    const sectionQs = questions.filter((q) => q.section === key);
    const visible = sectionQs.filter((q) => isQuestionVisible(q, responses));

    const fieldErrors: Record<string, string> = {};
    for (const q of visible) {
      const err = validateQuestion(q);
      if (err) fieldErrors[q.id] = err;
    }

    setErrors((prev) => ({
      ...stripSectionErrors(key, prev),
      ...fieldErrors,
    }));

    return Object.keys(fieldErrors).length === 0;
  }, [activeSectionIdx, questions, responses, stripSectionErrors, validateQuestion]);

  const handleResponseChange = (questionId: string, value: unknown) => {
    setResponses((prev) => ({
      ...prev,
      [questionId]: value,
    }));

    setErrors((prev) => {
      if (!prev[questionId]) return prev;
      const newErrors = { ...prev };
      delete newErrors[questionId];
      return newErrors;
    });
  };

  const completedBeforeActive = activeSectionIdx;

  const handleAdvanceSection = () => {
    if (!validateActiveSection()) return;

    if (activeSectionIdx >= SECTION_KEYS.length - 1) {
      void handleSubmitConfirmed();
      return;
    }
    setActiveSectionIdx((i) => Math.min(i + 1, SECTION_KEYS.length - 1));
  };

  const handleBackSection = () => {
    setErrors({});
    if (activeSectionIdx <= 0) {
      setFlowPhase('intent');
      return;
    }
    setActiveSectionIdx((i) => Math.max(i - 1, 0));
  };

  const handleSubmitConfirmed = async () => {
    setIsSubmitting(true);
    try {
      await onSubmit(responses);
    } catch (error) {
      console.error('Failed to submit questionnaire:', error);
    } finally {
      setIsSubmitting(false);
    }
  };

  const renderTierHint = (question: QuestionnaireQuestion) => {
    const tier = question.importance ?? (question.required ? 'mandatory' : 'recommended');
    if (tier === 'mandatory') {
      return <span className="text-muted-foreground font-normal"> (required)</span>;
    }
    const label =
      tier === 'recommended'
        ? 'Recommended'
        : tier === 'optional'
          ? 'Optional'
          : tier === 'advanced'
            ? 'Advanced'
            : tier;
    return (
      <span className="text-muted-foreground ml-1 text-xs font-normal normal-case">· {label}</span>
    );
  };

  const pillGridClass = 'flex flex-wrap gap-2';

  const renderDropdownControl = (
    question: QuestionnaireQuestion,
    value: unknown,
    error?: string,
    disabled?: boolean
  ) => {
    const opts = question.options ?? [];
    const strVal = asString(value);

    if (opts.length <= 6) {
      return (
        <div className={pillGridClass}>
          {opts.map((option) => {
            const selected = strVal === option;
            return (
              <button
                key={option}
                type="button"
                disabled={disabled}
                onClick={() => handleResponseChange(question.id, option)}
                className={cn(
                  'inline-flex items-center gap-2 rounded-full border px-4 py-2 text-sm transition-all duration-150',
                  selected
                    ? 'border-primary bg-primary text-primary-foreground shadow-sm'
                    : 'border border-border bg-background text-foreground hover:border-primary/50 hover:bg-primary/5 hover:text-primary',
                  error && !selected && 'border-destructive/60'
                )}
              >
                {selected && <Check className="h-3.5 w-3.5 shrink-0" />}
                <span>{option}</span>
              </button>
            );
          })}
        </div>
      );
    }

    return (
      <SearchableSelect
        id={question.id}
        options={opts}
        value={strVal}
        onChange={(v) => handleResponseChange(question.id, v)}
        error={Boolean(error)}
        disabled={disabled}
      />
    );
  };

  const renderCheckboxControl = (
    question: QuestionnaireQuestion,
    value: unknown,
    error?: string,
    disabled?: boolean
  ) => {
    const opts = question.options ?? [];
    const current = Array.isArray(value) ? (value as string[]) : [];

    return (
      <div className={pillGridClass}>
        {opts.map((option) => {
          const selected = current.includes(option);
          return (
            <button
              key={option}
              type="button"
              disabled={disabled}
              onClick={() => {
                if (selected) {
                  handleResponseChange(
                    question.id,
                    current.filter((x) => x !== option)
                  );
                } else {
                  handleResponseChange(question.id, [...current, option]);
                }
              }}
              className={cn(
                'inline-flex items-center gap-2 rounded-full border px-4 py-2 text-sm transition-all duration-150 text-left',
                selected
                  ? 'border-primary bg-primary text-primary-foreground shadow-sm'
                  : 'border border-border bg-background text-foreground hover:border-primary/50 hover:bg-primary/5 hover:text-primary',
                error && !selected && 'border-destructive/60'
              )}
            >
              {selected && <Check className="h-3.5 w-3.5 shrink-0" />}
              <span>{option}</span>
            </button>
          );
        })}
      </div>
    );
  };

  const renderQuestion = (question: QuestionnaireQuestion, visibleIndex: number) => {
    if (!isQuestionVisible(question, responses)) return null;

    const value = responses[question.id];
    const error = errors[question.id];
    const qMarker = (
      <span className="mb-2 block text-xs font-mono uppercase tracking-wider text-primary/70">
        Q{visibleIndex + 1}
      </span>
    );
    const inputSurface =
      'border-0 border-b border-input rounded-none bg-transparent px-0 shadow-none focus-visible:ring-0 focus-visible:border-primary';

    switch (question.type) {
      case 'text':
      case 'email':
      case 'phone':
      case 'date':
        return (
          <Card key={question.id} className={questionCardClass}>
            <CardContent className="space-y-2 pt-6">
              {qMarker}
              <Label htmlFor={question.id} className="text-lg font-semibold leading-snug text-foreground">
                {question.question}
                {renderTierHint(question)}
              </Label>
              <Input
                id={question.id}
                type={question.type}
                value={asString(value)}
                disabled={busy}
                onChange={(e) => handleResponseChange(question.id, e.target.value)}
                className={cn(inputSurface, error && 'border-destructive')}
              />
              {question.helpText && (
                <p className="mt-1.5 text-sm text-muted-foreground">{question.helpText}</p>
              )}
              {error && <p className="text-xs text-destructive">{error}</p>}
            </CardContent>
          </Card>
        );

      case 'number':
        return (
          <Card key={question.id} className={questionCardClass}>
            <CardContent className="space-y-2 pt-6">
              {qMarker}
              <Label htmlFor={question.id} className="text-lg font-semibold leading-snug text-foreground">
                {question.question}
                {renderTierHint(question)}
              </Label>
              <Input
                id={question.id}
                type="number"
                min={question.min}
                max={question.max}
                disabled={busy}
                value={asString(value)}
                onChange={(e) => {
                  const raw = e.target.value;
                  handleResponseChange(question.id, raw === '' ? '' : parseFloat(raw));
                }}
                className={cn(inputSurface, error && 'border-destructive')}
              />
              {question.helpText && (
                <p className="mt-1.5 text-sm text-muted-foreground">{question.helpText}</p>
              )}
              {error && <p className="text-xs text-destructive">{error}</p>}
            </CardContent>
          </Card>
        );

      case 'dropdown':
        return (
          <Card key={question.id} className={questionCardClass}>
            <CardContent className="space-y-3 pt-6">
              {qMarker}
              <Label htmlFor={question.id} className="text-lg font-semibold leading-snug text-foreground">
                {question.question}
                {renderTierHint(question)}
              </Label>
              {renderDropdownControl(question, value, error, busy)}
              {question.helpText && (
                <p className="mt-1.5 text-sm text-muted-foreground">{question.helpText}</p>
              )}
              {error && <p className="text-xs text-destructive">{error}</p>}
            </CardContent>
          </Card>
        );

      case 'slider': {
        const defaultSliderValue = Math.floor(((question.min || 1) + (question.max || 10)) / 2);
        const sliderValue = Array.isArray(value) ? value[0] : (value ?? defaultSliderValue);

        return (
          <Card key={question.id} className={questionCardClass}>
            <CardContent className="space-y-4 pt-6">
              {qMarker}
              <Label htmlFor={question.id} className="text-lg font-semibold leading-snug text-foreground">
                {question.question}
                {renderTierHint(question)}
              </Label>
              <div className="space-y-4">
                <div className="flex flex-wrap items-baseline gap-3">
                  <span className="text-5xl font-bold tabular-nums leading-none text-primary">{sliderValue}</span>
                  {question.labels?.[String(sliderValue)] != null ? (
                    <span className="text-sm text-muted-foreground">{question.labels[String(sliderValue)]}</span>
                  ) : null}
                </div>
                <div className={cn(busy && 'pointer-events-none opacity-60')}>
                  <Slider
                    min={question.min || 1}
                    max={question.max || 10}
                    step={1}
                    value={[sliderValue as number]}
                    onValueChange={(val) => handleResponseChange(question.id, val[0])}
                    className="w-full"
                  />
                </div>
                <div className="flex justify-between text-xs font-mono text-muted-foreground">
                  {question.labels && (
                    <>
                      <span>{question.labels[String(question.min || 1)]}</span>
                      <span>{question.labels[String(question.max || 10)]}</span>
                    </>
                  )}
                </div>
              </div>
              {question.helpText && (
                <p className="mt-1.5 text-sm text-muted-foreground">{question.helpText}</p>
              )}
              {error && <p className="text-xs text-destructive">{error}</p>}
            </CardContent>
          </Card>
        );
      }

      case 'checkbox':
        return (
          <Card key={question.id} className={questionCardClass}>
            <CardContent className="space-y-3 pt-6">
              {qMarker}
              <Label className="text-lg font-semibold leading-snug text-foreground">
                {question.question}
                {renderTierHint(question)}
              </Label>
              {renderCheckboxControl(question, value, error, busy)}
              {question.helpText && (
                <p className="mt-1.5 text-sm text-muted-foreground">{question.helpText}</p>
              )}
              {error && <p className="text-xs text-destructive">{error}</p>}
            </CardContent>
          </Card>
        );

      case 'group': {
        const groupObj = isRecord(value) ? value : {};
        return (
          <Card key={question.id} className={questionCardClass}>
            <CardContent className="space-y-3 pt-6">
              {qMarker}
              <Label className="text-lg font-semibold leading-snug text-foreground">
                {question.question}
                {renderTierHint(question)}
              </Label>
              <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
                {question.fields?.map((field) => (
                  <div key={field.label} className="space-y-1">
                    <Label htmlFor={`${question.id}-${field.label}`} className="text-xs text-muted-foreground">
                      {field.label}
                    </Label>
                    <Input
                      id={`${question.id}-${field.label}`}
                      type={field.type}
                      min={field.min}
                      max={field.max}
                      disabled={busy}
                      value={asString(groupObj[field.label])}
                      onChange={(e) => {
                        const parsed =
                          field.type === 'number'
                            ? e.target.value === ''
                              ? ''
                              : parseFloat(e.target.value)
                            : e.target.value;
                        handleResponseChange(question.id, {
                          ...groupObj,
                          [field.label]: parsed,
                        });
                      }}
                      className={cn(inputSurface)}
                    />
                  </div>
                ))}
              </div>
              {question.helpText && (
                <p className="mt-1.5 text-sm text-muted-foreground">{question.helpText}</p>
              )}
              {error && <p className="text-xs text-destructive">{error}</p>}
            </CardContent>
          </Card>
        );
      }

      default:
        return (
          <Card key={question.id} className={questionCardClass}>
            <CardContent className="space-y-2 pt-6">
              {qMarker}
              <Label htmlFor={question.id} className="text-lg font-semibold leading-snug text-foreground">
                {question.question}
                {renderTierHint(question)}
              </Label>
              <Textarea
                id={question.id}
                disabled={busy}
                value={asString(value)}
                onChange={(e) => handleResponseChange(question.id, e.target.value)}
                className={cn('min-h-[100px] border-border bg-background', error && 'border-destructive')}
              />
              {question.helpText && (
                <p className="mt-1.5 text-sm text-muted-foreground">{question.helpText}</p>
              )}
              {error && <p className="text-xs text-destructive">{error}</p>}
            </CardContent>
          </Card>
        );
    }
  };

  const intentSectionCards = (
    <div className="grid gap-3 sm:grid-cols-2">
      {sectionsOrdered.map(({ key, meta }, idx) => (
        <div
          key={key}
          style={{ animationDelay: `${idx * 60}ms` }}
          className={cn(
            'animate-fade-up relative cursor-default overflow-hidden rounded-xl border border-border bg-card p-5',
            'transition-all duration-200 hover:border-primary/40 hover:bg-primary/5',
            'before:pointer-events-none before:absolute before:bottom-0 before:left-0 before:top-0 before:w-0.5 before:bg-primary before:opacity-0 before:transition-opacity before:duration-200 hover:before:opacity-100'
          )}
        >
          <div className="flex items-start gap-3">
            <span className="text-3xl leading-none" aria-hidden>
              {meta.icon}
            </span>
            <div>
              <p className="text-base font-semibold text-foreground">{meta.label}</p>
              <p className="text-sm font-mono text-primary">{meta.estimate}</p>
            </div>
          </div>
        </div>
      ))}
    </div>
  );

  const sidebar = (
    <aside className="hidden w-[240px] shrink-0 flex-col border-r border-border bg-card lg:flex">
      <div className="border-b border-border px-5 py-5">
        <p className="text-sm font-bold uppercase tracking-[0.2em] text-foreground">HealthIQ</p>
        <p className="mt-0.5 text-xs text-muted-foreground">Calibration map</p>
      </div>
      <nav className="flex-1 space-y-1 px-3 py-4" aria-label="Questionnaire sections">
        {sectionsOrdered.map(({ key, meta }, idx) => {
          const isActive = idx === activeSectionIdx;
          const isDone = idx < completedBeforeActive;

          return (
            <button
              key={key}
              type="button"
              disabled={busy || flowPhase !== 'sections'}
              onClick={() => {
                if (flowPhase !== 'sections') return;
                if (idx <= activeSectionIdx) {
                  setActiveSectionIdx(idx);
                  setErrors({});
                }
              }}
              className={cn(
                'flex w-full items-center gap-3 rounded-lg px-3 py-2.5 text-left text-sm transition-colors',
                isActive && 'border border-primary/20 bg-primary/10 text-primary',
                !isActive && isDone && 'text-muted-foreground hover:bg-muted/50',
                !isActive && !isDone && 'text-muted-foreground/50',
                busy && 'opacity-60'
              )}
            >
              <span className="text-lg" aria-hidden>
                {meta.icon}
              </span>
              <span className="flex-1 font-medium">{meta.label}</span>
              {isDone && <Check className="h-4 w-4 shrink-0 text-primary" aria-label="Completed section" />}
            </button>
          );
        })}
      </nav>
      <div className="border-t border-border px-5 py-4">
        <p className="text-xs font-mono text-primary">
          {completedBeforeActive} of {SECTION_KEYS.length} sections complete
        </p>
      </div>
    </aside>
  );

  const mobileSectionStrip = (
    <div className="flex gap-2 overflow-x-auto pb-2 lg:hidden scrollbar-thin">
      {sectionsOrdered.map(({ key, meta }, idx) => {
        const isActive = idx === activeSectionIdx;
        const isDone = idx < completedBeforeActive;
        return (
          <button
            key={key}
            type="button"
            disabled={busy || flowPhase !== 'sections'}
            onClick={() => {
              if (flowPhase !== 'sections') return;
              if (idx <= activeSectionIdx) {
                setActiveSectionIdx(idx);
                setErrors({});
              }
            }}
            className={cn(
              'flex shrink-0 items-center gap-2 rounded-full border px-3 py-1.5 text-xs transition-colors',
              isActive && 'border-primary bg-primary/10 font-medium text-primary',
              !isActive && isDone && 'border-border bg-muted/50 text-muted-foreground',
              !isActive && !isDone && 'border-border/50 bg-transparent text-muted-foreground/60'
            )}
          >
            <span aria-hidden>{meta.icon}</span>
            <span className="max-w-[120px] truncate">{meta.label}</span>
          </button>
        );
      })}
    </div>
  );

  if (loadingQuestions) {
    return (
      <div className="flex items-center justify-center p-8">
        <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
        <span className="ml-2 text-muted-foreground">Loading questionnaire…</span>
      </div>
    );
  }

  if (schemaLoadError) {
    return (
      <div className="mx-auto max-w-4xl space-y-4 p-6">
        <Alert className="border-destructive/40 bg-destructive/10">
          <AlertCircle className="h-4 w-4 text-destructive" />
          <AlertDescription className="text-destructive">
            <strong>Could not load questionnaire.</strong> {schemaLoadError}
          </AlertDescription>
        </Alert>
        <Button type="button" onClick={() => void loadQuestions()} variant="outline">
          Retry
        </Button>
      </div>
    );
  }

  if (questions.length === 0) {
    return (
      <div className="mx-auto max-w-4xl p-6">
        <Alert>
          <AlertDescription>No questionnaire questions were returned from the server.</AlertDescription>
        </Alert>
      </div>
    );
  }

  if (flowPhase === 'intent') {
    return (
      <div className="relative min-h-screen w-full bg-background">
        <div
          className="pointer-events-none absolute inset-0"
          aria-hidden
          style={{
            background:
              'radial-gradient(ellipse 70% 50% at 100% 0%, hsl(142 76% 36% / 0.07) 0%, transparent 65%)',
          }}
        />
        <div className="relative z-10 mx-auto max-w-4xl px-4 py-8 sm:px-6">
          <div className="space-y-8">
            <header className="animate-fade-up space-y-3">
              <h1
                className={`${dmSerif.className} text-4xl font-normal leading-tight tracking-tight text-foreground sm:text-5xl lg:text-6xl`}
              >
                Let&apos;s calibrate
                <br />
                your analysis.
              </h1>
              <p className="max-w-xl text-lg leading-relaxed text-muted-foreground">
                These questions let us interpret your results as you — not as population averages. Answer honestly;
                precision improves your output.
              </p>
              <p className="text-sm font-mono text-primary">About 13 minutes · seven sections</p>
            </header>

            {intentSectionCards}

            <div className="flex flex-col gap-4 pt-2 sm:flex-row sm:items-center sm:justify-between">
              <Button
                type="button"
                disabled={busy}
                onClick={() => {
                  setFlowPhase('sections');
                  setActiveSectionIdx(0);
                }}
                className="h-14 min-w-[200px] rounded-xl bg-primary px-10 text-base font-semibold text-primary-foreground shadow-[0_0_24px_hsl(var(--primary)/0.35)] transition-all duration-300 hover:bg-primary-glow hover:shadow-[0_0_32px_hsl(var(--primary)/0.5)]"
              >
                Begin <ChevronRight className="ml-2 h-4 w-4" />
              </Button>
              {onCancel && (
                <button
                  type="button"
                  onClick={onCancel}
                  disabled={busy}
                  className="text-sm text-muted-foreground/60 underline-offset-4 transition-colors hover:text-muted-foreground hover:underline"
                >
                  Not now
                </button>
              )}
            </div>
          </div>
        </div>
      </div>
    );
  }

  const activeSection = sectionsOrdered[activeSectionIdx];

  return (
    <div className="mx-auto flex min-h-screen max-w-6xl flex-col bg-background lg:flex-row">
      {sidebar}

      <div className="flex min-w-0 flex-1 flex-col">
        <div className="border-b border-border border-t-[3px] border-t-primary px-4 py-6 sm:px-8">
          <div className="lg:hidden">{mobileSectionStrip}</div>
          <div className="mt-4 flex flex-wrap items-center gap-3 sm:mt-2">
            <span className="text-3xl leading-none" aria-hidden>
              {activeSection.meta.icon}
            </span>
            <div>
              <h2 className="text-2xl font-semibold tracking-tight text-foreground">{activeSection.meta.label}</h2>
              <p className="text-sm font-mono text-primary">{activeSection.meta.estimate}</p>
            </div>
          </div>
        </div>

        <div className="flex flex-1 flex-col px-4 py-8 sm:px-8">
          <div key={activeSectionIdx} className="animate-fade-up mx-auto flex w-full max-w-2xl flex-1 flex-col space-y-6">
            {activeSection.questions
              .filter((q) => isQuestionVisible(q, responses))
              .map((q, qi) => renderQuestion(q, qi))}

            <div className="flex flex-col-reverse gap-3 border-t border-border pt-8 sm:flex-row sm:justify-between">
              <Button type="button" variant="outline" onClick={handleBackSection} disabled={busy}>
                ← Back
              </Button>
              {activeSectionIdx >= SECTION_KEYS.length - 1 ? (
                <Button
                  type="button"
                  onClick={handleAdvanceSection}
                  disabled={busy}
                  className="h-12 bg-primary px-8 font-semibold text-primary-foreground shadow-[0_0_20px_hsl(var(--primary)/0.3)] transition-all duration-300 hover:bg-primary-glow hover:shadow-[0_0_28px_hsl(var(--primary)/0.45)]"
                >
                  Unlock my analysis
                  <ChevronRight className="ml-2 h-4 w-4" />
                </Button>
              ) : (
                <Button
                  type="button"
                  onClick={handleAdvanceSection}
                  disabled={busy}
                  className="h-12 px-8 font-semibold"
                >
                  Next section
                  <ChevronRight className="ml-2 h-4 w-4" />
                </Button>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

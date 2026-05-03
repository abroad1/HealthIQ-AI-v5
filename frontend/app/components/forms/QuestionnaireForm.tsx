'use client';

import React, { useState, useEffect, useCallback, useMemo, useRef } from 'react';
import { Manrope, JetBrains_Mono } from 'next/font/google';
import { motion } from 'framer-motion';
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

/** Single sans family for the whole questionnaire — avoids Times-like serifs + futuristic display clashes */
const fontSans = Manrope({
  subsets: ['latin'],
  weight: ['400', '500', '600', '700', '800'],
  display: 'swap',
});

/** Readouts only (Q#, durations, diagnostics) — never mixed as a headline pair */
const fontMono = JetBrains_Mono({
  subsets: ['latin'],
  weight: ['400', '500'],
  display: 'swap',
});

const motionEase = [0.22, 1, 0.36, 1] as const;

const motionStaggerParent = {
  hidden: {},
  show: {
    transition: { staggerChildren: 0.085, delayChildren: 0.06 },
  },
};

const motionStaggerItem = {
  hidden: { opacity: 0, y: 18 },
  show: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.44, ease: motionEase },
  },
};

/** Instrument panel — gradient wash + primary spine, not flat Card */
const questionCardClass =
  'relative overflow-hidden rounded-2xl border border-border/60 bg-gradient-to-br from-card via-card to-muted/20 shadow-sm transition-[box-shadow,border-color] duration-300 hover:border-primary/25 hover:shadow-[0_12px_40px_-16px_hsl(var(--primary)/0.12)] before:pointer-events-none before:absolute before:inset-y-4 before:left-0 before:w-[3px] before:rounded-full before:bg-gradient-to-b before:from-primary before:to-primary/40';

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
          fontSans.className,
          'flex h-11 w-full items-center justify-between rounded-lg border border-border/80 bg-background/80 px-3 text-left text-[13px] font-medium tracking-wide backdrop-blur-[2px] transition-all duration-200 hover:border-primary/45 hover:bg-primary/[0.04]',
          error ? 'border-destructive' : 'border-input/80',
          disabled && 'cursor-not-allowed opacity-60'
        )}
      >
        <span className={cn(!value && 'text-muted-foreground')}>{value || placeholder}</span>
        <ChevronRight className={cn('h-4 w-4 shrink-0 rotate-90 text-muted-foreground transition-transform', open && 'rotate-[270deg]')} />
      </button>
      {open && (
        <div className="absolute left-0 right-0 top-full z-50 mt-1 rounded-xl border border-border/80 bg-popover/95 p-2 shadow-xl backdrop-blur-md">
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
                  fontSans.className,
                  'flex w-full items-center rounded-lg px-2 py-2.5 text-left text-[13px] font-medium tracking-wide transition-colors hover:bg-accent/80',
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

  const renderRequiredHint = (question: QuestionnaireQuestion) =>
    question.required ? (
      <span className={cn(fontMono.className, 'text-[10px] font-medium uppercase tracking-[0.14em] text-muted-foreground/80')}>
        {' '}
        · required
      </span>
    ) : null;

  const pillGridClass = 'flex flex-wrap gap-2.5';

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
                  fontSans.className,
                  'inline-flex items-center gap-2 rounded-xl border px-5 py-2.5 text-[13px] font-semibold tracking-wide transition-all duration-200',
                  selected
                    ? 'border-primary bg-primary text-primary-foreground shadow-[0_4px_24px_-6px_hsl(var(--primary)/0.55)]'
                    : 'border-border/90 bg-background/60 text-foreground shadow-sm hover:border-primary/40 hover:bg-primary/[0.06] hover:text-primary',
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
                fontSans.className,
                'inline-flex items-center gap-2 rounded-xl border px-5 py-2.5 text-[13px] font-semibold tracking-wide transition-all duration-200 text-left',
                selected
                  ? 'border-primary bg-primary text-primary-foreground shadow-[0_4px_24px_-6px_hsl(var(--primary)/0.55)]'
                  : 'border-border/90 bg-background/60 text-foreground shadow-sm hover:border-primary/40 hover:bg-primary/[0.06] hover:text-primary',
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
      <span
        className={cn(
          fontMono.className,
          'mb-3 block text-[11px] font-medium uppercase tracking-[0.2em] text-primary/75'
        )}
      >
        Q{visibleIndex + 1}
      </span>
    );
    const inputSurface =
      'border-0 border-b border-input/70 rounded-none bg-transparent px-0 font-medium shadow-none transition-colors focus-visible:border-primary focus-visible:ring-0';

    switch (question.type) {
      case 'text':
      case 'email':
      case 'phone':
      case 'date':
        return (
          <Card key={question.id} className={questionCardClass}>
            <CardContent className="space-y-3 px-8 pb-8 pt-9">
              {qMarker}
              <Label
                htmlFor={question.id}
                className={cn(
                  fontSans.className,
                  'block text-xl font-semibold leading-[1.35] tracking-tight text-foreground md:text-[1.375rem]'
                )}
              >
                {question.question}
                {renderRequiredHint(question)}
              </Label>
              <Input
                id={question.id}
                type={question.type}
                value={asString(value)}
                disabled={busy}
                onChange={(e) => handleResponseChange(question.id, e.target.value)}
                className={cn(fontSans.className, inputSurface, error && 'border-destructive')}
              />
              {question.helpText && (
                <p className={cn(fontSans.className, 'mt-2 text-[0.8125rem] leading-relaxed text-muted-foreground/90')}>
                  {question.helpText}
                </p>
              )}
              {error && <p className={cn(fontMono.className, 'text-xs font-medium text-destructive')}>{error}</p>}
            </CardContent>
          </Card>
        );

      case 'number':
        return (
          <Card key={question.id} className={questionCardClass}>
            <CardContent className="space-y-3 px-8 pb-8 pt-9">
              {qMarker}
              <Label
                htmlFor={question.id}
                className={cn(
                  fontSans.className,
                  'block text-xl font-semibold leading-[1.35] tracking-tight text-foreground md:text-[1.375rem]'
                )}
              >
                {question.question}
                {renderRequiredHint(question)}
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
                className={cn(fontSans.className, inputSurface, error && 'border-destructive')}
              />
              {question.helpText && (
                <p className={cn(fontSans.className, 'mt-2 text-[0.8125rem] leading-relaxed text-muted-foreground/90')}>
                  {question.helpText}
                </p>
              )}
              {error && <p className={cn(fontMono.className, 'text-xs font-medium text-destructive')}>{error}</p>}
            </CardContent>
          </Card>
        );

      case 'dropdown':
        return (
          <Card key={question.id} className={questionCardClass}>
            <CardContent className="space-y-4 px-8 pb-8 pt-9">
              {qMarker}
              <Label
                htmlFor={question.id}
                className={cn(
                  fontSans.className,
                  'block text-xl font-semibold leading-[1.35] tracking-tight text-foreground md:text-[1.375rem]'
                )}
              >
                {question.question}
                {renderRequiredHint(question)}
              </Label>
              {renderDropdownControl(question, value, error, busy)}
              {question.helpText && (
                <p className={cn(fontSans.className, 'mt-2 text-[0.8125rem] leading-relaxed text-muted-foreground/90')}>
                  {question.helpText}
                </p>
              )}
              {error && <p className={cn(fontMono.className, 'text-xs font-medium text-destructive')}>{error}</p>}
            </CardContent>
          </Card>
        );

      case 'slider': {
        const defaultSliderValue = Math.floor(((question.min || 1) + (question.max || 10)) / 2);
        const sliderValue = Array.isArray(value) ? value[0] : (value ?? defaultSliderValue);

        return (
          <Card key={question.id} className={questionCardClass}>
            <CardContent className="space-y-5 px-8 pb-8 pt-9">
              {qMarker}
              <Label
                htmlFor={question.id}
                className={cn(
                  fontSans.className,
                  'block text-xl font-semibold leading-[1.35] tracking-tight text-foreground md:text-[1.375rem]'
                )}
              >
                {question.question}
                {renderRequiredHint(question)}
              </Label>
              <div className="space-y-5">
                <div className="flex flex-wrap items-end gap-x-4 gap-y-2 border-b border-border/50 pb-5">
                  <span
                    className={cn(
                      fontMono.className,
                      'text-6xl font-bold tabular-nums leading-none tracking-tight text-primary md:text-7xl'
                    )}
                  >
                    {sliderValue}
                  </span>
                  {question.labels?.[String(sliderValue)] != null ? (
                    <span className={cn(fontSans.className, 'max-w-md pb-1 text-sm italic text-muted-foreground/90')}>
                      {question.labels[String(sliderValue)]}
                    </span>
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
                <div className={cn(fontMono.className, 'flex justify-between text-[11px] font-medium uppercase tracking-wider text-muted-foreground/75')}>
                  {question.labels && (
                    <>
                      <span>{question.labels[String(question.min || 1)]}</span>
                      <span>{question.labels[String(question.max || 10)]}</span>
                    </>
                  )}
                </div>
              </div>
              {question.helpText && (
                <p className={cn(fontSans.className, 'mt-2 text-[0.8125rem] leading-relaxed text-muted-foreground/90')}>
                  {question.helpText}
                </p>
              )}
              {error && <p className={cn(fontMono.className, 'text-xs font-medium text-destructive')}>{error}</p>}
            </CardContent>
          </Card>
        );
      }

      case 'checkbox':
        return (
          <Card key={question.id} className={questionCardClass}>
            <CardContent className="space-y-4 px-8 pb-8 pt-9">
              {qMarker}
              <Label
                className={cn(
                  fontSans.className,
                  'block text-xl font-semibold leading-[1.35] tracking-tight text-foreground md:text-[1.375rem]'
                )}
              >
                {question.question}
                {renderRequiredHint(question)}
              </Label>
              {renderCheckboxControl(question, value, error, busy)}
              {question.helpText && (
                <p className={cn(fontSans.className, 'mt-2 text-[0.8125rem] leading-relaxed text-muted-foreground/90')}>
                  {question.helpText}
                </p>
              )}
              {error && <p className={cn(fontMono.className, 'text-xs font-medium text-destructive')}>{error}</p>}
            </CardContent>
          </Card>
        );

      case 'group': {
        const groupObj = isRecord(value) ? value : {};
        return (
          <Card key={question.id} className={questionCardClass}>
            <CardContent className="space-y-4 px-8 pb-8 pt-9">
              {qMarker}
              <Label
                className={cn(
                  fontSans.className,
                  'block text-xl font-semibold leading-[1.35] tracking-tight text-foreground md:text-[1.375rem]'
                )}
              >
                {question.question}
                {renderRequiredHint(question)}
              </Label>
              <div className="grid grid-cols-1 gap-6 sm:grid-cols-2">
                {question.fields?.map((field) => (
                  <div key={field.label} className="space-y-2">
                    <Label
                      htmlFor={`${question.id}-${field.label}`}
                      className={cn(
                        fontMono.className,
                        'text-[10px] font-semibold uppercase tracking-[0.16em] text-muted-foreground/80'
                      )}
                    >
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
                      className={cn(fontSans.className, inputSurface)}
                    />
                  </div>
                ))}
              </div>
              {question.helpText && (
                <p className={cn(fontSans.className, 'mt-2 text-[0.8125rem] leading-relaxed text-muted-foreground/90')}>
                  {question.helpText}
                </p>
              )}
              {error && <p className={cn(fontMono.className, 'text-xs font-medium text-destructive')}>{error}</p>}
            </CardContent>
          </Card>
        );
      }

      default:
        return (
          <Card key={question.id} className={questionCardClass}>
            <CardContent className="space-y-3 px-8 pb-8 pt-9">
              {qMarker}
              <Label
                htmlFor={question.id}
                className={cn(
                  fontSans.className,
                  'block text-xl font-semibold leading-[1.35] tracking-tight text-foreground md:text-[1.375rem]'
                )}
              >
                {question.question}
                {renderRequiredHint(question)}
              </Label>
              <Textarea
                id={question.id}
                disabled={busy}
                value={asString(value)}
                onChange={(e) => handleResponseChange(question.id, e.target.value)}
                className={cn(
                  fontSans.className,
                  'min-h-[120px] rounded-xl border border-border/70 bg-background/50 px-4 py-3 text-[15px] leading-relaxed shadow-inner transition-colors focus-visible:border-primary focus-visible:ring-1 focus-visible:ring-primary/25',
                  error && 'border-destructive'
                )}
              />
              {question.helpText && (
                <p className={cn(fontSans.className, 'mt-2 text-[0.8125rem] leading-relaxed text-muted-foreground/90')}>
                  {question.helpText}
                </p>
              )}
              {error && <p className={cn(fontMono.className, 'text-xs font-medium text-destructive')}>{error}</p>}
            </CardContent>
          </Card>
        );
    }
  };

  const intentSectionCards = (
    <motion.div
      initial="hidden"
      animate="show"
      variants={motionStaggerParent}
      className="grid gap-4 sm:grid-cols-2 lg:gap-5"
    >
      {sectionsOrdered.map(({ key, meta }) => (
        <motion.div
          key={key}
          variants={motionStaggerItem}
          className={cn(
            'relative cursor-default overflow-hidden rounded-2xl border border-border/70 bg-card/90 p-6 shadow-sm backdrop-blur-[1px]',
            'transition-[border-color,box-shadow,background-color] duration-300 hover:border-primary/35 hover:bg-primary/[0.04] hover:shadow-[0_20px_50px_-28px_hsl(var(--primary)/0.25)]',
            'before:pointer-events-none before:absolute before:bottom-0 before:left-0 before:top-0 before:w-[3px] before:bg-gradient-to-b before:from-primary before:to-primary/30 before:opacity-0 before:transition-opacity before:duration-300 hover:before:opacity-100'
          )}
        >
          <div className="flex items-start gap-4">
            <span className="select-none text-[2rem] leading-none opacity-90" aria-hidden>
              {meta.icon}
            </span>
            <div className="min-w-0 space-y-1">
              <p className={cn(fontSans.className, 'text-[1.35rem] font-bold leading-tight tracking-tight text-foreground sm:text-2xl')}>
                {meta.label}
              </p>
              <p className={cn(fontMono.className, 'text-[12px] font-medium tracking-wide text-primary')}>{meta.estimate}</p>
            </div>
          </div>
        </motion.div>
      ))}
    </motion.div>
  );

  const sidebar = (
    <aside className="relative hidden w-[280px] shrink-0 flex-col border-r border-primary/12 bg-gradient-to-b from-card via-card to-muted/30 lg:flex lg:shadow-[inset_-1px_0_0_0_hsl(var(--border)/0.45)]">
      <div className="border-b border-border/80 px-6 py-6">
        <p className={cn(fontSans.className, 'text-sm font-bold tracking-tight text-foreground')}>HealthIQ</p>
        <p className={cn(fontMono.className, 'mt-2 text-[10px] font-medium uppercase tracking-[0.18em] text-muted-foreground/85')}>
          Calibration map
        </p>
      </div>
      <nav className="flex-1 space-y-1.5 px-4 py-5" aria-label="Questionnaire sections">
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
                fontSans.className,
                'flex w-full items-center gap-3 rounded-xl px-3.5 py-3 text-left text-[13px] font-semibold tracking-wide transition-all duration-200',
                isActive &&
                  'border border-primary/35 bg-gradient-to-r from-primary/14 to-primary/[0.06] text-primary shadow-[inset_0_0_0_1px_hsl(var(--primary)/0.12)]',
                !isActive && isDone && 'text-muted-foreground hover:bg-muted/60',
                !isActive && !isDone && 'text-muted-foreground/45',
                busy && 'opacity-60'
              )}
            >
              <span className="text-xl opacity-90" aria-hidden>
                {meta.icon}
              </span>
              <span className="flex-1 leading-snug">{meta.label}</span>
              {isDone && <Check className="h-4 w-4 shrink-0 text-primary" aria-label="Completed section" />}
            </button>
          );
        })}
      </nav>
      <div className="border-t border-border/80 px-6 py-5">
        <p className={cn(fontMono.className, 'text-[11px] font-semibold uppercase tracking-[0.12em] text-primary/90')}>
          {completedBeforeActive} of {SECTION_KEYS.length} sections complete
        </p>
      </div>
    </aside>
  );

  const mobileSectionStrip = (
    <div className="flex gap-2 overflow-x-auto pb-3 pt-1 lg:hidden scrollbar-thin">
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
              fontSans.className,
              'flex shrink-0 items-center gap-2 rounded-xl border px-3.5 py-2 text-[11px] font-bold tracking-wide transition-all duration-200',
              isActive &&
                'border-primary/40 bg-gradient-to-br from-primary/15 to-primary/[0.05] text-primary shadow-sm',
              !isActive && isDone && 'border-border/80 bg-muted/40 text-muted-foreground',
              !isActive && !isDone && 'border-border/40 bg-transparent text-muted-foreground/55'
            )}
          >
            <span aria-hidden>{meta.icon}</span>
            <span className="max-w-[132px] truncate">{meta.label}</span>
          </button>
        );
      })}
    </div>
  );

  if (loadingQuestions) {
    return (
      <div className={cn(fontSans.className, 'flex items-center justify-center p-10 antialiased')}>
        <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
        <span className="ml-3 text-sm font-semibold tracking-wide text-muted-foreground">Loading questionnaire…</span>
      </div>
    );
  }

  if (schemaLoadError) {
    return (
      <div className={cn(fontSans.className, 'mx-auto max-w-4xl space-y-4 p-6 antialiased')}>
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
      <div className={cn(fontSans.className, 'mx-auto max-w-4xl p-6 antialiased')}>
        <Alert>
          <AlertDescription>No questionnaire questions were returned from the server.</AlertDescription>
        </Alert>
      </div>
    );
  }

  if (flowPhase === 'intent') {
    return (
      <div className={cn(fontSans.className, 'relative min-h-screen w-full bg-background antialiased')}>
        <div
          className="pointer-events-none absolute inset-0"
          aria-hidden
          style={{
            background:
              'radial-gradient(ellipse 85% 55% at 100% -10%, hsl(142 76% 38% / 0.09) 0%, transparent 55%), radial-gradient(ellipse 60% 45% at 0% 100%, hsl(142 76% 38% / 0.045) 0%, transparent 50%)',
          }}
        />
        <div className="relative z-10 mx-auto max-w-[52rem] px-5 py-12 sm:px-10 sm:py-16 lg:py-20">
          <motion.div className="space-y-12" initial="hidden" animate="show" variants={motionStaggerParent}>
            <motion.header variants={motionStaggerItem} className="max-w-2xl space-y-6">
              <h1
                className={cn(
                  fontSans.className,
                  'text-[2.65rem] font-extrabold leading-[1.08] tracking-tight text-foreground sm:text-6xl lg:text-[4.25rem]'
                )}
              >
                Let&apos;s calibrate
                <br />
                your analysis.
              </h1>
              <p className={cn(fontSans.className, 'max-w-xl text-lg font-medium leading-relaxed text-muted-foreground sm:text-xl')}>
                These questions let us interpret your results as you — not as population averages. Answer honestly;
                precision improves your output.
              </p>
              <p className={cn(fontMono.className, 'text-[13px] font-semibold uppercase tracking-[0.14em] text-primary')}>
                About 13 minutes · seven sections
              </p>
            </motion.header>

            <motion.div variants={motionStaggerItem}>{intentSectionCards}</motion.div>

            <motion.div
              variants={motionStaggerItem}
              className="flex flex-col gap-6 pt-2 sm:flex-row sm:items-end sm:justify-between"
            >
              <Button
                type="button"
                disabled={busy}
                onClick={() => {
                  setFlowPhase('sections');
                  setActiveSectionIdx(0);
                }}
                className={cn(
                  fontSans.className,
                  'h-[3.75rem] min-w-[220px] rounded-2xl bg-primary px-12 text-[15px] font-bold uppercase tracking-[0.08em] text-primary-foreground shadow-[0_0_36px_hsl(var(--primary)/0.38)] transition-all duration-300 hover:bg-primary-glow hover:shadow-[0_0_48px_hsl(var(--primary)/0.52)]'
                )}
              >
                Begin <ChevronRight className="ml-2 h-4 w-4" />
              </Button>
              {onCancel && (
                <button
                  type="button"
                  onClick={onCancel}
                  disabled={busy}
                  className={cn(
                    fontMono.className,
                    'text-[11px] font-medium uppercase tracking-[0.14em] text-muted-foreground/55 underline-offset-[6px] transition-colors hover:text-muted-foreground hover:underline'
                  )}
                >
                  Not now
                </button>
              )}
            </motion.div>
          </motion.div>
        </div>
      </div>
    );
  }

  const activeSection = sectionsOrdered[activeSectionIdx];

  return (
    <div
      className={cn(
        fontSans.className,
        'relative mx-auto flex min-h-screen w-full max-w-[1180px] flex-col bg-background antialiased lg:flex-row'
      )}
    >
      <div
        className="pointer-events-none absolute inset-0 lg:left-[280px]"
        aria-hidden
        style={{
          background:
            'radial-gradient(ellipse 75% 55% at 85% 5%, hsl(var(--primary) / 0.055) 0%, transparent 52%)',
        }}
      />

      {sidebar}

      <div className="relative flex min-w-0 flex-1 flex-col">
        <div className="border-b border-border/70 border-t-[3px] border-t-primary px-6 py-8 sm:px-10 sm:py-10 lg:pl-14 lg:pr-16">
          <div className="lg:hidden">{mobileSectionStrip}</div>
          <div className="mt-6 flex flex-wrap items-end gap-5 sm:mt-4 lg:mt-2">
            <span className="select-none text-[2.75rem] leading-none opacity-90" aria-hidden>
              {activeSection.meta.icon}
            </span>
            <div className="min-w-0 space-y-2">
              <p className={cn(fontMono.className, 'text-[10px] font-semibold uppercase tracking-[0.22em] text-muted-foreground/75')}>
                Active calibration stage
              </p>
              <h2 className={cn(fontSans.className, 'text-[2rem] font-bold tracking-tight text-foreground md:text-[2.35rem]')}>
                {activeSection.meta.label}
              </h2>
              <p className={cn(fontMono.className, 'text-[13px] font-semibold tracking-wide text-primary')}>
                {activeSection.meta.estimate}
              </p>
            </div>
          </div>
        </div>

        <div className="flex flex-1 flex-col px-6 pb-16 pt-10 sm:px-10 lg:pl-14 lg:pr-16 lg:pb-20 lg:pt-12">
          <motion.div
            key={activeSectionIdx}
            initial={{ opacity: 0, y: 14 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.42, ease: motionEase }}
            className="mx-auto flex w-full max-w-[36rem] flex-1 flex-col space-y-8 lg:mx-0 lg:max-w-[40rem]"
          >
            {activeSection.questions
              .filter((q) => isQuestionVisible(q, responses))
              .map((q, qi) => renderQuestion(q, qi))}

            <div className="flex flex-col-reverse gap-4 border-t border-border/70 pt-10 sm:flex-row sm:justify-between">
              <Button
                type="button"
                variant="outline"
                onClick={handleBackSection}
                disabled={busy}
                className={cn(fontSans.className, 'rounded-xl border-border/90 px-6 py-6 text-[13px] font-bold uppercase tracking-[0.12em]')}
              >
                ← Back
              </Button>
              {activeSectionIdx >= SECTION_KEYS.length - 1 ? (
                <Button
                  type="button"
                  onClick={handleAdvanceSection}
                  disabled={busy}
                  className={cn(
                    fontSans.className,
                    'h-[3rem] rounded-xl bg-primary px-10 text-[13px] font-bold uppercase tracking-[0.12em] text-primary-foreground shadow-[0_0_28px_hsl(var(--primary)/0.34)] transition-all duration-300 hover:bg-primary-glow hover:shadow-[0_0_40px_hsl(var(--primary)/0.48)]'
                  )}
                >
                  Unlock my analysis
                  <ChevronRight className="ml-2 h-4 w-4" />
                </Button>
              ) : (
                <Button
                  type="button"
                  onClick={handleAdvanceSection}
                  disabled={busy}
                  className={cn(
                    fontSans.className,
                    'h-[3rem] rounded-xl px-10 text-[13px] font-bold uppercase tracking-[0.12em]'
                  )}
                >
                  Next section
                  <ChevronRight className="ml-2 h-4 w-4" />
                </Button>
              )}
            </div>
          </motion.div>
        </div>
      </div>
    </div>
  );
}

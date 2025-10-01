import React, { createContext, useContext, useState, ReactNode } from "react";

interface SelectContextType {
  value: string | undefined;
  onValueChange: (value: string) => void;
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

const SelectContext = createContext<SelectContextType | undefined>(undefined);

export interface SelectProps {
  value?: string;
  onValueChange?: (value: string) => void;
  children: ReactNode;
}

export function Select({ value, onValueChange, children }: SelectProps) {
  const [open, setOpen] = useState(false);
  
  return (
    <SelectContext.Provider value={{ 
      value, 
      onValueChange: onValueChange || (() => {}), 
      open, 
      onOpenChange: setOpen 
    }}>
      <div className="relative">
        {children}
      </div>
    </SelectContext.Provider>
  );
}

export interface SelectTriggerProps {
  children: ReactNode;
  className?: string;
}

export function SelectTrigger({ children, className = "" }: SelectTriggerProps) {
  const context = useContext(SelectContext);
  if (!context) {
    throw new Error("SelectTrigger must be used within a Select component");
  }

  return (
    <button
      className={`flex h-10 w-full items-center justify-between rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 ${className}`}
      onClick={() => context.onOpenChange(!context.open)}
    >
      {children}
      <svg width="12" height="12" viewBox="0 0 12 12" fill="none" className="h-4 w-4 opacity-50">
        <path d="M6 9L1.5 4.5H10.5L6 9Z" fill="currentColor"/>
      </svg>
    </button>
  );
}

export interface SelectValueProps {
  placeholder?: string;
  className?: string;
}

export function SelectValue({ placeholder, className = "" }: SelectValueProps) {
  const context = useContext(SelectContext);
  if (!context) {
    throw new Error("SelectValue must be used within a Select component");
  }

  return (
    <span className={`block truncate ${className}`}>
      {context.value || placeholder}
    </span>
  );
}

export interface SelectContentProps {
  children: ReactNode;
  className?: string;
}

export function SelectContent({ children, className = "" }: SelectContentProps) {
  const context = useContext(SelectContext);
  if (!context) {
    throw new Error("SelectContent must be used within a Select component");
  }

  if (!context.open) {
    return null;
  }

  return (
    <div className={`absolute top-full left-0 z-50 w-full mt-1 max-h-60 overflow-auto rounded-md border bg-popover text-popover-foreground shadow-lg ${className}`}>
      {children}
    </div>
  );
}

export interface SelectItemProps {
  value: string;
  children: ReactNode;
  className?: string;
}

export function SelectItem({ value, children, className = "" }: SelectItemProps) {
  const context = useContext(SelectContext);
  if (!context) {
    throw new Error("SelectItem must be used within a Select component");
  }

  const isSelected = context.value === value;

  return (
    <div
      className={`relative flex cursor-default select-none items-center rounded-sm py-1.5 pl-8 pr-2 text-sm outline-none hover:bg-accent hover:text-accent-foreground ${
        isSelected ? "bg-accent text-accent-foreground" : ""
      } ${className}`}
      onClick={() => {
        context.onValueChange(value);
        context.onOpenChange(false);
      }}
    >
      {isSelected && (
        <span className="absolute left-2 flex h-3.5 w-3.5 items-center justify-center">
          <svg width="12" height="12" viewBox="0 0 12 12" fill="none" className="h-4 w-4">
            <path d="M10 3L4.5 8.5L2 6" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
        </span>
      )}
      {children}
    </div>
  );
}
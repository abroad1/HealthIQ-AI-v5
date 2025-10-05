import React, { createContext, useContext, useState, ReactNode } from "react";

interface CollapsibleContextType {
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

const CollapsibleContext = createContext<CollapsibleContextType | undefined>(undefined);

export interface CollapsibleProps {
  open?: boolean;
  onOpenChange?: (open: boolean) => void;
  children: ReactNode;
  className?: string;
}

export function Collapsible({ open: controlledOpen, onOpenChange, children, className = "" }: CollapsibleProps) {
  const [internalOpen, setInternalOpen] = useState(false);
  const open = controlledOpen !== undefined ? controlledOpen : internalOpen;
  const handleOpenChange = onOpenChange || setInternalOpen;

  return (
    <CollapsibleContext.Provider value={{ open, onOpenChange: handleOpenChange }}>
      <div className={className}>
        {children}
      </div>
    </CollapsibleContext.Provider>
  );
}

export interface CollapsibleTriggerProps {
  asChild?: boolean;
  children: ReactNode;
  className?: string;
}

export function CollapsibleTrigger({ asChild = false, children, className = "" }: CollapsibleTriggerProps) {
  const context = useContext(CollapsibleContext);
  if (!context) {
    throw new Error("CollapsibleTrigger must be used within a Collapsible component");
  }

  const handleClick = () => {
    context.onOpenChange(!context.open);
  };

  if (asChild && React.isValidElement(children)) {
    return React.cloneElement(children as React.ReactElement<any>, {
      onClick: handleClick,
      className: `${(children as React.ReactElement<any>).props.className || ""} ${className}`.trim()
    });
  }

  return (
    <button
      className={`cursor-pointer ${className}`}
      onClick={handleClick}
    >
      {children}
    </button>
  );
}

export interface CollapsibleContentProps {
  children: ReactNode;
  className?: string;
}

export function CollapsibleContent({ children, className = "" }: CollapsibleContentProps) {
  const context = useContext(CollapsibleContext);
  if (!context) {
    throw new Error("CollapsibleContent must be used within a Collapsible component");
  }

  if (!context.open) {
    return null;
  }

  return (
    <div className={`overflow-hidden transition-all duration-300 ease-in-out ${className}`}>
      {children}
    </div>
  );
}

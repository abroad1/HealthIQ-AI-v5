import React from 'react';

interface SelectProps extends React.SelectHTMLAttributes<HTMLSelectElement> {
  children: React.ReactNode;
  onValueChange?: (value: string) => void;
}

export const Select = React.forwardRef<HTMLSelectElement, SelectProps>(
  ({ className = '', children, onValueChange, onChange, ...props }, ref) => {
    const handleChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
      onValueChange?.(e.target.value);
      onChange?.(e);
    };

    return (
      <select
        className={`flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 ${className}`}
        ref={ref}
        onChange={handleChange}
        {...props}
      >
        {children}
      </select>
    );
  }
);

Select.displayName = 'Select';

interface SelectContentProps {
  children: React.ReactNode;
}

export const SelectContent = ({ children }: SelectContentProps) => {
  return <>{children}</>;
};

interface SelectItemProps extends React.OptionHTMLAttributes<HTMLOptionElement> {
  children: React.ReactNode;
  value: string;
}

export const SelectItem = React.forwardRef<HTMLOptionElement, SelectItemProps>(
  ({ children, ...props }, ref) => (
    <option ref={ref} {...props}>
      {children}
    </option>
  )
);

SelectItem.displayName = 'SelectItem';

interface SelectTriggerProps extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode;
}

export const SelectTrigger = React.forwardRef<HTMLDivElement, SelectTriggerProps>(
  ({ className = '', children, ...props }, ref) => (
    <div
      ref={ref}
      className={`flex h-10 w-full items-center justify-between rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 ${className}`}
      {...props}
    >
      {children}
    </div>
  )
);

SelectTrigger.displayName = 'SelectTrigger';

interface SelectValueProps {
  placeholder?: string;
}

export const SelectValue = ({ placeholder }: SelectValueProps) => {
  return <span className="text-muted-foreground">{placeholder}</span>;
};

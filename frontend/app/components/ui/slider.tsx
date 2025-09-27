import React from 'react';

interface SliderProps extends React.InputHTMLAttributes<HTMLInputElement> {
  min?: number;
  max?: number;
  step?: number;
  value?: number;
  onValueChange?: (value: number) => void;
}

export const Slider = React.forwardRef<HTMLInputElement, SliderProps>(
  ({ className = '', min = 0, max = 100, step = 1, value, onValueChange, ...props }, ref) => {
    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
      const newValue = parseInt(e.target.value);
      onValueChange?.(newValue);
    };

    return (
      <input
        type="range"
        min={min}
        max={max}
        step={step}
        value={value}
        onChange={handleChange}
        className={`w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer ${className}`}
        ref={ref}
        {...props}
      />
    );
  }
);

Slider.displayName = 'Slider';

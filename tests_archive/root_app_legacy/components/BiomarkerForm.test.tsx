import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import BiomarkerForm from '@/app/components/forms/BiomarkerForm';

// Mock the UI components
jest.mock('@/components/ui/card', () => ({
  Card: ({ children, className }: any) => <div className={className}>{children}</div>,
  CardContent: ({ children, className }: any) => <div className={className}>{children}</div>,
  CardDescription: ({ children, className }: any) => <div className={className}>{children}</div>,
  CardHeader: ({ children, className }: any) => <div className={className}>{children}</div>,
  CardTitle: ({ children, className }: any) => <h3 className={className}>{children}</h3>,
}));

jest.mock('@/components/ui/button', () => ({
  Button: ({ children, onClick, disabled, className, ...props }: any) => (
    <button onClick={onClick} disabled={disabled} className={className} {...props}>
      {children}
    </button>
  ),
}));

jest.mock('@/components/ui/input', () => ({
  Input: ({ onChange, value, type, ...props }: any) => (
    <input onChange={onChange} value={value} type={type} {...props} />
  ),
}));

jest.mock('@/components/ui/label', () => ({
  Label: ({ children, htmlFor, className }: any) => (
    <label htmlFor={htmlFor} className={className}>{children}</label>
  ),
}));

jest.mock('@/components/ui/select', () => ({
  Select: ({ children, value, onValueChange }: any) => (
    <select value={value} onChange={(e) => onValueChange(e.target.value)}>
      {children}
    </select>
  ),
  SelectContent: ({ children }: any) => <div>{children}</div>,
  SelectItem: ({ children, value }: any) => <option value={value}>{children}</option>,
  SelectTrigger: ({ children, className }: any) => <div className={className}>{children}</div>,
  SelectValue: ({ placeholder }: any) => <span>{placeholder}</span>,
}));

jest.mock('@/components/ui/tabs', () => ({
  Tabs: ({ children, value, onValueChange }: any) => (
    <div data-testid="tabs" data-value={value} data-onchange={onValueChange}>
      {children}
    </div>
  ),
  TabsContent: ({ children, value }: any) => (
    <div data-testid={`tab-content-${value}`}>{children}</div>
  ),
  TabsList: ({ children, className }: any) => (
    <div className={className} data-testid="tabs-list">{children}</div>
  ),
  TabsTrigger: ({ children, value, className }: any) => (
    <button data-testid={`tab-trigger-${value}`} className={className}>
      {children}
    </button>
  ),
}));

describe('BiomarkerForm', () => {
  const mockOnSubmit = jest.fn();
  const mockOnCancel = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders the form with manual entry tab by default', () => {
    render(<BiomarkerForm onSubmit={mockOnSubmit} onCancel={mockOnCancel} />);
    
    expect(screen.getByText('Enter Biomarker Values')).toBeInTheDocument();
    expect(screen.getByText('Add Biomarker')).toBeInTheDocument();
    expect(screen.getByText('No biomarkers added yet')).toBeInTheDocument();
  });

  it('allows adding biomarkers', async () => {
    const user = userEvent.setup();
    render(<BiomarkerForm onSubmit={mockOnSubmit} onCancel={mockOnCancel} />);
    
    const addButton = screen.getByText('Add Biomarker');
    await user.click(addButton);
    
    expect(screen.getByText('Biomarker')).toBeInTheDocument();
    expect(screen.getByText('Value')).toBeInTheDocument();
    expect(screen.getByText('Unit')).toBeInTheDocument();
  });

  it('validates required fields before submission', async () => {
    const user = userEvent.setup();
    render(<BiomarkerForm onSubmit={mockOnSubmit} onCancel={mockOnCancel} />);
    
    // Add a biomarker but don't fill required fields
    const addButton = screen.getByText('Add Biomarker');
    await user.click(addButton);
    
    const submitButton = screen.getByText('Submit 1 Biomarkers');
    await user.click(submitButton);
    
    // Should not call onSubmit
    expect(mockOnSubmit).not.toHaveBeenCalled();
  });

  it('submits valid biomarker data', async () => {
    const user = userEvent.setup();
    render(<BiomarkerForm onSubmit={mockOnSubmit} onCancel={mockOnCancel} />);
    
    // Add a biomarker
    const addButton = screen.getByText('Add Biomarker');
    await user.click(addButton);
    
    // Fill in the biomarker data
    const biomarkerSelect = screen.getByDisplayValue('Select biomarker');
    await user.selectOptions(biomarkerSelect, 'glucose');
    
    const valueInput = screen.getByDisplayValue('');
    await user.type(valueInput, '100');
    
    const unitSelect = screen.getByDisplayValue('Select unit');
    await user.selectOptions(unitSelect, 'mg/dL');
    
    const submitButton = screen.getByText('Submit 1 Biomarkers');
    await user.click(submitButton);
    
    expect(mockOnSubmit).toHaveBeenCalledWith({
      glucose: {
        value: 100,
        unit: 'mg/dL',
        date: expect.any(String)
      }
    });
  });

  it('allows removing biomarkers', async () => {
    const user = userEvent.setup();
    render(<BiomarkerForm onSubmit={mockOnSubmit} onCancel={mockOnCancel} />);
    
    // Add a biomarker
    const addButton = screen.getByText('Add Biomarker');
    await user.click(addButton);
    
    // Remove the biomarker
    const removeButton = screen.getByRole('button', { name: /trash/i });
    await user.click(removeButton);
    
    expect(screen.getByText('No biomarkers added yet')).toBeInTheDocument();
  });

  it('switches between manual entry and CSV upload tabs', async () => {
    const user = userEvent.setup();
    render(<BiomarkerForm onSubmit={mockOnSubmit} onCancel={mockOnCancel} />);
    
    // Switch to CSV upload tab
    const uploadTab = screen.getByText('CSV Upload');
    await user.click(uploadTab);
    
    expect(screen.getByText('Upload CSV File')).toBeInTheDocument();
    expect(screen.getByText('Choose CSV File')).toBeInTheDocument();
  });

  it('handles CSV file upload', async () => {
    const user = userEvent.setup();
    render(<BiomarkerForm onSubmit={mockOnSubmit} onCancel={mockOnCancel} />);
    
    // Switch to CSV upload tab
    const uploadTab = screen.getByText('CSV Upload');
    await user.click(uploadTab);
    
    // Create a mock CSV file
    const csvContent = 'glucose,100,mg/dL,2024-01-01\nhba1c,5.5,%,2024-01-01';
    const file = new File([csvContent], 'test.csv', { type: 'text/csv' });
    
    const fileInput = screen.getByLabelText('Choose CSV File');
    await user.upload(fileInput, file);
    
    // Should show success message
    await waitFor(() => {
      expect(screen.getByText('CSV file processed. 2 biomarkers loaded.')).toBeInTheDocument();
    });
  });

  it('shows loading state when submitting', () => {
    render(<BiomarkerForm onSubmit={mockOnSubmit} onCancel={mockOnCancel} isLoading={true} />);
    
    expect(screen.getByText('Processing...')).toBeInTheDocument();
  });

  it('calls onCancel when cancel button is clicked', async () => {
    const user = userEvent.setup();
    render(<BiomarkerForm onSubmit={mockOnSubmit} onCancel={mockOnCancel} />);
    
    const cancelButton = screen.getByText('Cancel');
    await user.click(cancelButton);
    
    expect(mockOnCancel).toHaveBeenCalled();
  });

  it('disables submit button when no biomarkers are added', () => {
    render(<BiomarkerForm onSubmit={mockOnSubmit} onCancel={mockOnCancel} />);
    
    const submitButton = screen.getByText('Submit 0 Biomarkers');
    expect(submitButton).toBeDisabled();
  });

  it('shows correct biomarker count in submit button', async () => {
    const user = userEvent.setup();
    render(<BiomarkerForm onSubmit={mockOnSubmit} onCancel={mockOnCancel} />);
    
    // Add two biomarkers
    const addButton = screen.getByText('Add Biomarker');
    await user.click(addButton);
    await user.click(addButton);
    
    expect(screen.getByText('Submit 2 Biomarkers')).toBeInTheDocument();
  });
});

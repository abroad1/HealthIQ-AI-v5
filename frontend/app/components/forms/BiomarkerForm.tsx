'use client';

import React, { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Upload, Database, AlertCircle, CheckCircle, Plus, Trash2 } from 'lucide-react';

interface BiomarkerValue {
  id: string;
  value: number;
  unit: string;
  date?: string;
}

interface BiomarkerFormProps {
  onSubmit: (data: any) => void;
  onCancel?: () => void;
  isLoading?: boolean;
  showSubmitButton?: boolean;
}

// Common biomarkers with their units and reference ranges
const BIOMARKER_DEFINITIONS = {
  // Metabolic
  glucose: { name: 'Glucose', units: ['mg/dL', 'mmol/L'], category: 'metabolic' },
  hba1c: { name: 'HbA1c', units: ['%', 'mmol/mol'], category: 'metabolic' },
  insulin: { name: 'Insulin', units: ['μU/mL', 'pmol/L'], category: 'metabolic' },
  c_peptide: { name: 'C-Peptide', units: ['ng/mL', 'nmol/L'], category: 'metabolic' },
  
  // Cardiovascular
  total_cholesterol: { name: 'Total Cholesterol', units: ['mg/dL', 'mmol/L'], category: 'cardiovascular' },
  ldl_cholesterol: { name: 'LDL Cholesterol', units: ['mg/dL', 'mmol/L'], category: 'cardiovascular' },
  hdl_cholesterol: { name: 'HDL Cholesterol', units: ['mg/dL', 'mmol/L'], category: 'cardiovascular' },
  triglycerides: { name: 'Triglycerides', units: ['mg/dL', 'mmol/L'], category: 'cardiovascular' },
  apolipoprotein_b: { name: 'Apolipoprotein B', units: ['mg/dL', 'g/L'], category: 'cardiovascular' },
  apolipoprotein_a1: { name: 'Apolipoprotein A1', units: ['mg/dL', 'g/L'], category: 'cardiovascular' },
  
  // Inflammatory
  crp: { name: 'C-Reactive Protein (CRP)', units: ['mg/L', 'mg/dL'], category: 'inflammatory' },
  esr: { name: 'Erythrocyte Sedimentation Rate (ESR)', units: ['mm/hr'], category: 'inflammatory' },
  il_6: { name: 'Interleukin-6 (IL-6)', units: ['pg/mL', 'ng/L'], category: 'inflammatory' },
  tnf_alpha: { name: 'TNF-α', units: ['pg/mL', 'ng/L'], category: 'inflammatory' },
  
  // Organ Function
  creatinine: { name: 'Creatinine', units: ['mg/dL', 'μmol/L'], category: 'organ' },
  bun: { name: 'Blood Urea Nitrogen (BUN)', units: ['mg/dL', 'mmol/L'], category: 'organ' },
  alt: { name: 'ALT (Alanine Aminotransferase)', units: ['U/L'], category: 'organ' },
  ast: { name: 'AST (Aspartate Aminotransferase)', units: ['U/L'], category: 'organ' },
  ggt: { name: 'GGT (Gamma-Glutamyl Transferase)', units: ['U/L'], category: 'organ' },
  alkaline_phosphatase: { name: 'Alkaline Phosphatase', units: ['U/L'], category: 'organ' },
  
  // CBC
  hemoglobin: { name: 'Hemoglobin', units: ['g/dL', 'g/L'], category: 'cbc' },
  hematocrit: { name: 'Hematocrit', units: ['%', 'L/L'], category: 'cbc' },
  wbc: { name: 'White Blood Cell Count', units: ['K/μL', '×10⁹/L'], category: 'cbc' },
  rbc: { name: 'Red Blood Cell Count', units: ['M/μL', '×10¹²/L'], category: 'cbc' },
  platelets: { name: 'Platelet Count', units: ['K/μL', '×10⁹/L'], category: 'cbc' },
  
  // Hormonal
  tsh: { name: 'TSH (Thyroid Stimulating Hormone)', units: ['mIU/L', 'μIU/mL'], category: 'hormonal' },
  free_t4: { name: 'Free T4', units: ['ng/dL', 'pmol/L'], category: 'hormonal' },
  free_t3: { name: 'Free T3', units: ['pg/mL', 'pmol/L'], category: 'hormonal' },
  cortisol: { name: 'Cortisol', units: ['μg/dL', 'nmol/L'], category: 'hormonal' },
  testosterone: { name: 'Testosterone', units: ['ng/dL', 'nmol/L'], category: 'hormonal' },
  
  // Nutritional
  vitamin_d: { name: 'Vitamin D (25-OH)', units: ['ng/mL', 'nmol/L'], category: 'nutritional' },
  vitamin_b12: { name: 'Vitamin B12', units: ['pg/mL', 'pmol/L'], category: 'nutritional' },
  folate: { name: 'Folate', units: ['ng/mL', 'nmol/L'], category: 'nutritional' },
  iron: { name: 'Iron', units: ['μg/dL', 'μmol/L'], category: 'nutritional' },
  ferritin: { name: 'Ferritin', units: ['ng/mL', 'μg/L'], category: 'nutritional' }
};

const CATEGORY_LABELS = {
  metabolic: 'Metabolic Health',
  cardiovascular: 'Cardiovascular Health',
  inflammatory: 'Inflammatory Health',
  organ: 'Organ Function',
  cbc: 'Complete Blood Count',
  hormonal: 'Hormonal Health',
  nutritional: 'Nutritional Status'
};

export default function BiomarkerForm({ 
  onSubmit, 
  onCancel, 
  isLoading = false,
  showSubmitButton = true 
}: BiomarkerFormProps) {
  const [biomarkers, setBiomarkers] = useState<BiomarkerValue[]>([]);
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [activeTab, setActiveTab] = useState<string>('manual');
  const [csvData, setCsvData] = useState<string>('');

  const addBiomarker = () => {
    const newBiomarker: BiomarkerValue = {
      id: '',
      value: 0,
      unit: '',
      date: new Date().toISOString().split('T')[0]
    };
    setBiomarkers([...biomarkers, newBiomarker]);
  };

  const removeBiomarker = (index: number) => {
    setBiomarkers(biomarkers.filter((_, i) => i !== index));
  };

  const updateBiomarker = (index: number, field: keyof BiomarkerValue, value: any) => {
    const updated = [...biomarkers];
    updated[index] = { ...updated[index], [field]: value };
    setBiomarkers(updated);
    
    // Clear error for this biomarker
    if (errors[`biomarker_${index}`]) {
      setErrors(prev => {
        const newErrors = { ...prev };
        delete newErrors[`biomarker_${index}`];
        return newErrors;
      });
    }
  };

  const validateForm = () => {
    const newErrors: Record<string, string> = {};
    
    biomarkers.forEach((biomarker, index) => {
      if (!biomarker.id) {
        newErrors[`biomarker_${index}`] = 'Please select a biomarker';
      }
      if (!biomarker.value || biomarker.value <= 0) {
        newErrors[`biomarker_${index}`] = 'Please enter a valid value';
      }
      if (!biomarker.unit) {
        newErrors[`biomarker_${index}`] = 'Please select a unit';
      }
    });

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = () => {
    if (!validateForm()) {
      return;
    }

    const formattedData = biomarkers.reduce((acc, biomarker) => {
      acc[biomarker.id] = {
        value: biomarker.value,
        unit: biomarker.unit,
        date: biomarker.date
      };
      return acc;
    }, {} as Record<string, any>);

    onSubmit(formattedData);
  };

  const handleCsvUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (e) => {
      const content = e.target?.result as string;
      setCsvData(content);
      parseCsvData(content);
    };
    reader.readAsText(file);
  };

  const parseCsvData = (csvContent: string) => {
    const lines = csvContent.split('\n').filter(line => line.trim());
    const headers = lines[0].split(',').map(h => h.trim().toLowerCase());
    
    const parsedBiomarkers: BiomarkerValue[] = [];
    
    for (let i = 1; i < lines.length; i++) {
      const values = lines[i].split(',').map(v => v.trim());
      
      if (values.length >= 2) {
        const biomarkerId = values[0].toLowerCase().replace(/[^a-z0-9_]/g, '_');
        const value = parseFloat(values[1]);
        const unit = values[2] || '';
        const date = values[3] || new Date().toISOString().split('T')[0];
        
        if (!isNaN(value)) {
          parsedBiomarkers.push({
            id: biomarkerId,
            value,
            unit,
            date
          });
        }
      }
    }
    
    setBiomarkers(parsedBiomarkers);
  };

  const getBiomarkersByCategory = () => {
    const categories: Record<string, string[]> = {};
    
    Object.entries(BIOMARKER_DEFINITIONS).forEach(([id, def]) => {
      if (!categories[def.category]) {
        categories[def.category] = [];
      }
      categories[def.category].push(id);
    });
    
    return categories;
  };

  const biomarkersByCategory = getBiomarkersByCategory();

  return (
    <div className="space-y-6">
      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList className="grid w-full grid-cols-2">
          <TabsTrigger value="manual" className="flex items-center gap-2">
            <Database className="h-4 w-4" />
            Manual Entry
          </TabsTrigger>
          <TabsTrigger value="upload" className="flex items-center gap-2">
            <Upload className="h-4 w-4" />
            CSV Upload
          </TabsTrigger>
        </TabsList>

        <TabsContent value="manual" className="space-y-4">
          <div className="flex justify-between items-center">
            <h3 className="text-lg font-semibold">Enter Biomarker Values</h3>
            <Button onClick={addBiomarker} size="sm" className="flex items-center gap-2">
              <Plus className="h-4 w-4" />
              Add Biomarker
            </Button>
          </div>

          {biomarkers.length === 0 ? (
            <Card className="border-dashed">
              <CardContent className="pt-6">
                <div className="text-center py-8">
                  <Database className="h-12 w-12 text-gray-300 mx-auto mb-4" />
                  <p className="text-gray-500 mb-4">No biomarkers added yet</p>
                  <Button onClick={addBiomarker} variant="outline">
                    Add Your First Biomarker
                  </Button>
                </div>
              </CardContent>
            </Card>
          ) : (
            <div className="space-y-4">
              {biomarkers.map((biomarker, index) => (
                <Card key={index} className="border-l-4 border-l-blue-500">
                  <CardContent className="pt-4">
                    <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                      <div>
                        <Label htmlFor={`biomarker-${index}`}>Biomarker</Label>
                        <Select
                          value={biomarker.id}
                          onValueChange={(value) => updateBiomarker(index, 'id', value)}
                        >
                          <SelectTrigger>
                            <SelectValue placeholder="Select biomarker" />
                          </SelectTrigger>
                          <SelectContent className="max-h-60">
                            {Object.entries(biomarkersByCategory).map(([category, biomarkerIds]) => (
                              <div key={category}>
                                <div className="px-2 py-1 text-xs font-semibold text-gray-500 bg-gray-50">
                                  {CATEGORY_LABELS[category as keyof typeof CATEGORY_LABELS]}
                                </div>
                                {biomarkerIds.map(id => (
                                  <SelectItem key={id} value={id}>
                                    {BIOMARKER_DEFINITIONS[id as keyof typeof BIOMARKER_DEFINITIONS]?.name}
                                  </SelectItem>
                                ))}
                              </div>
                            ))}
                          </SelectContent>
                        </Select>
                        {errors[`biomarker_${index}`] && (
                          <p className="text-xs text-red-500 mt-1">{errors[`biomarker_${index}`]}</p>
                        )}
                      </div>

                      <div>
                        <Label htmlFor={`value-${index}`}>Value</Label>
                        <Input
                          id={`value-${index}`}
                          type="number"
                          step="0.01"
                          value={biomarker.value || ''}
                          onChange={(e) => updateBiomarker(index, 'value', parseFloat(e.target.value))}
                          placeholder="Enter value"
                        />
                      </div>

                      <div>
                        <Label htmlFor={`unit-${index}`}>Unit</Label>
                        <Select
                          value={biomarker.unit}
                          onValueChange={(value) => updateBiomarker(index, 'unit', value)}
                        >
                          <SelectTrigger>
                            <SelectValue placeholder="Select unit" />
                          </SelectTrigger>
                          <SelectContent>
                            {biomarker.id && BIOMARKER_DEFINITIONS[biomarker.id as keyof typeof BIOMARKER_DEFINITIONS]?.units.map(unit => (
                              <SelectItem key={unit} value={unit}>{unit}</SelectItem>
                            ))}
                          </SelectContent>
                        </Select>
                      </div>

                      <div className="flex items-end">
                        <Button
                          type="button"
                          variant="outline"
                          size="sm"
                          onClick={() => removeBiomarker(index)}
                          className="text-red-600 hover:text-red-700"
                          aria-label="Remove biomarker"
                        >
                          <Trash2 className="h-4 w-4" />
                        </Button>
                      </div>
                    </div>

                    <div className="mt-3">
                      <Label htmlFor={`date-${index}`}>Date (Optional)</Label>
                      <Input
                        id={`date-${index}`}
                        type="date"
                        value={biomarker.date || ''}
                        onChange={(e) => updateBiomarker(index, 'date', e.target.value)}
                        className="max-w-xs"
                      />
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          )}
        </TabsContent>

        <TabsContent value="upload" className="space-y-4">
          <div>
            <h3 className="text-lg font-semibold mb-4">Upload CSV File</h3>
            <Card className="border-dashed">
              <CardContent className="pt-6">
                <div className="text-center">
                  <Upload className="h-12 w-12 text-gray-300 mx-auto mb-4" />
                  <p className="text-gray-600 mb-4">
                    Upload a CSV file with your biomarker data. Format: biomarker_id, value, unit, date
                  </p>
                  <input
                    type="file"
                    accept=".csv"
                    onChange={handleCsvUpload}
                    className="hidden"
                    id="csv-upload"
                  />
                  <Label htmlFor="csv-upload">
                    <Button variant="outline" onClick={() => document.getElementById('csv-upload')?.click()}>
                      Choose CSV File
                    </Button>
                  </Label>
                </div>
              </CardContent>
            </Card>

            {csvData && (
              <Alert>
                <CheckCircle className="h-4 w-4" />
                <AlertDescription>
                  CSV file processed. {biomarkers.length} biomarkers loaded.
                </AlertDescription>
              </Alert>
            )}
          </div>
        </TabsContent>
      </Tabs>

      {showSubmitButton && (
        <div className="flex justify-between pt-6">
          <Button
            variant="outline"
            onClick={onCancel}
            disabled={isLoading}
          >
            Cancel
          </Button>
          <Button
            onClick={handleSubmit}
            disabled={isLoading || biomarkers.length === 0}
            className="bg-blue-600 hover:bg-blue-700"
          >
            {isLoading ? 'Processing...' : `Submit ${biomarkers.length} Biomarkers`}
          </Button>
        </div>
      )}
    </div>
  );
}

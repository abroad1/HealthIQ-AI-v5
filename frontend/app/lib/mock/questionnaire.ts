export const mockQuestionnaire = {
  // Demographics Section
  full_name: "John Smith",
  email_address: "test@example.com",
  phone_number: "07123456789",
  country: "United Kingdom",
  state_province: "London",
  date_of_birth: "1978-05-15", // Makes them 45 years old (as of 2025)
  biological_sex: "Male",
  height: {
    Feet: 5,
    Inches: 10
  },
  weight: 165, // lbs
  
  // Lifestyle Section
  sleep_hours_nightly: "7-8 hours",
  sleep_quality_rating: 7,
  alcohol_drinks_weekly: "4-7 drinks",
  tobacco_use: "Never used",
  stress_level_rating: 5,
  vigorous_exercise_days: "3 days",
  
  // Medical History Section
  current_medications: "None",
  long_term_medications: ["None"],
  chronic_conditions: ["None"],
  medical_conditions: ["None"],
  
  // Symptoms Section
  current_symptoms: ["None"],
  regular_migraines: "No"
};

export default mockQuestionnaire;


export const getAllBills = () => {
  return [
    {
      id: 1,
      title: "Renewable Energy Incentive Act",
      summary: "Provides tax incentives for renewable energy companies.",
      sector: "Energy",
      sentiment: "Positive",
      impact: "High",
    },
    {
      id: 2,
      title: "Big Tech Regulation Act",
      summary: "Stricter regulations on tech monopolies.",
      sector: "Technology",
      sentiment: "Negative",
      impact: "Medium",
    },
    {
      id: 3,
      title: "Healthcare Affordability Act",
      summary: "Expands access to affordable healthcare services.",
      sector: "Healthcare",
      sentiment: "Positive",
      impact: "Low",
    },
  ];
};

export const billsData = [
  {
    id: 1,
    title: "Increased Corporate Tax Congress Bill 2024",
    summary: "Increases corporate tax rates for large businesses.",
    sector: "Finance",
    sentiment: "Negative",
    impact: "High",
    justification: "This bill increases corporate taxes, which may reduce profits and investment in large firms.",
    confidence: 0.91,
    stage: "Passed House"  // 👈 This is crucial!
  },
  
  // ... more bills
];

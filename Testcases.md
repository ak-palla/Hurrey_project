# Example Testcases

This document provides example test cases demonstrating the capabilities of the Individualized Chatbot with RAG Personalization, including persona configurations, document sources, and example interactions.

## Test Case 1: Technical Documentation Explainer

### Persona Configuration

| Parameter | Value | Description |
|-----------|-------|-------------|
| Tone | Friendly | Approachable and conversational |
| Goal | Educate | Focus on explaining concepts clearly |
| Length | Medium | Balanced detail and conciseness |
| Style | Step-by-Step | Structured, procedural explanations |
| Language | English | Standard English language |
| Persona | Beginner | Assumes limited technical background |

![Technical Documentation Explainer Persona](images/persona_technical_explainer.png)

### RAG Source Document

**Document**: Python_Basics.pdf

```
# Python Basics: A Quick Reference Guide

## Variables and Data Types

Python has several built-in data types:
- Integers (int): Whole numbers like 5, -3, 0
- Floating point (float): Decimal numbers like 5.6, -2.1
- Strings (str): Text enclosed in quotes like "Hello" or 'World'
- Booleans (bool): True or False values
- Lists: Ordered collections of items like [1, 2, 3]
- Dictionaries: Key-value pairs like {"name": "John", "age": 30}
- Tuples: Immutable ordered collections like (1, 2, 3)
- Sets: Unordered collections of unique items like {1, 2, 3}

## Control Flow

### Conditional Statements
```if condition:
    # do something
elif another_condition:
    # do something else
else:
    # do yet another thing```

### Loops
```# For loop
for item in iterable:
    # do something with item

# While loop
while condition:
    # do something
    # update condition```

## Functions

```def function_name(parameters):
    # function body
    return value```

Functions are defined using the `def` keyword followed by a function name and parameters.
```

### Sample Query and Response

**User Query**: 
```
What are the basic data types in Python? Can you explain them in simple terms?
```

**Chatbot Response**:
```
# Python's Basic Data Types Explained

Based on the document I have, Python has several built-in data types. Let me explain them in simple terms:

## Step 1: Numbers
- **Integers (int)**: These are whole numbers without decimal points. Examples: 5, -3, 0
- **Floating point (float)**: These are numbers with decimal points. Examples: 5.6, -2.1

## Step 2: Text
- **Strings (str)**: This is any text enclosed in quotes. Examples: "Hello" or 'World'

## Step 3: True/False Values
- **Booleans (bool)**: These represent logical values - either True or False

## Step 4: Collections of Items
- **Lists**: These are ordered collections of items that can be changed. Example: [1, 2, 3]
- **Dictionaries**: These store key-value pairs, like a real dictionary. Example: {"name": "John", "age": 30}
- **Tuples**: Similar to lists but cannot be changed after creation. Example: (1, 2, 3)
- **Sets**: Collections where each item appears only once. Example: {1, 2, 3}

Is there a specific data type you'd like me to explain in more detail?
```

### Screenshot

![Technical Explainer Test Case](images/testcase1_screenshot.png)

## Test Case 2: Scientific Research Summarizer

### Persona Configuration

| Parameter | Value | Description |
|-----------|-------|-------------|
| Tone | Professional | Formal and academically appropriate |
| Goal | Summarize | Focus on condensing complex information |
| Length | Detailed | Comprehensive but focused |
| Style | Analytical | Evidence-based with clear structure |
| Language | English | Standard English with technical vocabulary |
| Persona | Expert | Assumes advanced domain knowledge |

![Scientific Research Summarizer Persona](images/persona_research_summarizer.png)

### RAG Source Document

**Document**: Climate_Change_Research.pdf

```
# Recent Advances in Climate Change Research

## Abstract
This paper reviews recent findings in climate science from 2020-2023, focusing on three key areas: atmospheric carbon dioxide concentration, global temperature anomalies, and sea level rise. We synthesize data from multiple sources including satellite measurements, weather stations, and ocean buoys to provide a comprehensive overview of current climate trends.

## 1. Introduction
Climate change continues to be one of the most pressing environmental challenges of the 21st century. Understanding current trends is essential for effective policy decisions and mitigation strategies. This review compiles the latest data to present an updated picture of climate indicators.

## 2. Methods
Data was collected from NASA's Global Climate Change portal, NOAA's National Centers for Environmental Information, and the Intergovernmental Panel on Climate Change (IPCC) Sixth Assessment Report. Statistical analysis was performed using R (version 4.1.2) with significance levels set at p<0.05.

## 3. Results

### 3.1 Atmospheric CO2 Concentration
As of January 2023, atmospheric CO2 reached 419.5 ppm at the Mauna Loa Observatory, representing a 50% increase from pre-industrial levels of approximately 280 ppm. The rate of increase has accelerated to 2.5 ppm per year during the last decade, compared to 1.5 ppm per year in the 1990s.

### 3.2 Global Temperature Anomalies
The global average temperature for 2022 was 1.11°C above the pre-industrial baseline (1850-1900), making it the sixth warmest year on record. The ten warmest years have all occurred since 2010. Regional variations show more pronounced warming in the Arctic (approximately 3°C above baseline) and less pronounced warming in parts of the Southern Ocean (approximately 0.5°C above baseline).

### 3.3 Sea Level Rise
Global mean sea level has risen by 101.2 mm since 1993 based on satellite altimetry data, with an acceleration from 2.1 mm/year in the 1990s to 4.0 mm/year during 2010-2022. Thermal expansion accounts for approximately 50% of observed sea level rise, with glacier and ice sheet melt contributing the remainder.

## 4. Discussion
The acceleration of key climate indicators suggests that climate change is proceeding faster than projected in earlier IPCC reports. Of particular concern is the acceleration in sea level rise, which poses significant risks to coastal communities worldwide. Current trajectories indicate that without immediate and substantial reductions in greenhouse gas emissions, global warming is likely to exceed 1.5°C above pre-industrial levels by the early 2030s.

## 5. Conclusion
Recent data confirms the continued warming of the Earth's climate system at an accelerating rate. These findings underscore the urgent need for enhanced mitigation efforts and adaptation strategies to address the growing challenges posed by climate change.
```

### Sample Query and Response

**User Query**: 
```
What does the research say about sea level rise and its implications? Can you provide the specific data points?
```

**Chatbot Response**:
```
# Sea Level Rise: Research Findings and Implications

## Key Data Points on Sea Level Rise

The research document provides several specific measurements regarding sea level rise:

- Global mean sea level has risen by 101.2 mm (approximately 4 inches) since 1993 based on satellite altimetry data
- There has been a clear acceleration in the rate of sea level rise:
  * 2.1 mm/year in the 1990s
  * 4.0 mm/year during 2010-2022 (nearly double the previous rate)
- The composition of sea level rise includes:
  * Approximately 50% from thermal expansion of ocean water
  * Approximately 50% from glacier and ice sheet melt

## Implications

The research indicates several significant implications:

1. The acceleration of sea level rise is of "particular concern" as it poses "significant risks to coastal communities worldwide"

2. Sea level rise is occurring faster than projected in earlier IPCC reports, suggesting climate models may have been conservative in their estimates

3. This acceleration aligns with other accelerating climate indicators, suggesting a broader pattern of climate change proceeding more rapidly than previously anticipated

4. The research connects this acceleration to the urgent need for both:
   * Enhanced mitigation efforts (reducing greenhouse gas emissions)
   * Adaptation strategies (preparing for unavoidable sea level rise)

5. Without immediate action, the research suggests global warming will exceed 1.5°C above pre-industrial levels by the early 2030s, potentially further accelerating sea level rise

This evidence underscores the importance of addressing both the causes and consequences of sea level rise as part of comprehensive climate policy.
```

### Screenshot

![Scientific Research Test Case](images/testcase2_screenshot.png)

## Test Case 3: Dynamic Mood Override

This test case demonstrates how the chatbot can switch tones dynamically using the mood override feature.

### Base Persona Configuration

| Parameter | Value |
|-----------|-------|
| Tone | Professional |
| Goal | Advise |
| Length | Medium |
| Style | Straightforward |
| Language | English |
| Persona | Intermediate |

### Mood Override Test

**Initial Query**: 
```
What are some strategies for effective time management?
```

**Response (Professional Tone)**:
```
Based on the research in productivity and time management, here are effective strategies to consider:

1. Prioritize tasks using methodologies like the Eisenhower Matrix (urgent/important framework)
2. Implement time-blocking in your calendar for focused work periods
3. Identify and minimize time-wasting activities through periodic time audits
4. Use the Pomodoro Technique (25-minute focused work followed by 5-minute breaks)
5. Set clear boundaries between work and personal time
6. Delegate tasks that don't require your specific expertise
7. Batch similar tasks together to reduce context switching
8. Build in buffer time between commitments to avoid cascading delays

Consider tracking your implementation of these strategies to identify which ones provide the most benefit for your specific working style and responsibilities.
```

**Apply "Motivational" Mood Override**

![Mood Override Selection](images/mood_override_selection.png)

**Follow-up Query**:
```
Now tell me again about time management strategies
```

**Response (Motivational Tone)**:
```
You've got this! Time management isn't just about squeezing more tasks into your day—it's about taking control of your life and creating space for what truly matters to YOU!

Your journey to better time management starts with believing in yourself. When you prioritize your tasks, you're making powerful choices about what deserves your precious energy. Time-blocking isn't just a technique—it's a commitment to your goals and dreams!

I believe in you! When you minimize distractions and focus deeply using methods like the Pomodoro Technique, you're honoring your potential. Each focused session is a step toward becoming your best self.

Remember, setting boundaries isn't selfish—it's an act of self-respect! When you protect your time, you're saying "my goals matter" and that's something to be proud of.

The path to better time management isn't always easy, but I know you have the strength to transform how you use your time. Start small, celebrate your victories, and watch as you build momentum toward an intentional, fulfilling life where YOU are in control of your time!

What one strategy will you commit to trying today? The power to change is within you!
```

### Screenshot

![Mood Override Test Case](images/testcase3_screenshot.png)

## Test Case 4: Multi-Document Query

This test case demonstrates the chatbot's ability to retrieve information across multiple uploaded documents.

### Persona Configuration

| Parameter | Value |
|-----------|-------|
| Tone | Friendly |
| Goal | Explain |
| Length | Detailed |
| Style | Storytelling |
| Language | English |
| Persona | Beginner |

### RAG Source Documents

**Document 1**: renewable_energy.pdf  
**Document 2**: energy_policy.txt

### Sample Query and Response

**User Query**: 
```
Compare solar and wind energy advantages and disadvantages. What policies support them?
```

**Chatbot Response**:
```
# The Tale of Sun and Wind: Renewable Energy's Dynamic Duo

Imagine two friends named Solar and Wind who both want to help power our world without hurting the environment. They each have their own special powers and challenges, and governments have created special rules to help them succeed. Let me tell you their story!

## Solar's Shining Qualities
Our friend Solar harnesses the sun's abundant energy that bathes our planet every day. Solar has some impressive advantages:
- Creates no pollution while operating
- Works silently without disturbing neighbors
- Requires minimal maintenance once installed
- Can be installed on existing buildings or unused land
- Provides predictable daytime energy production
- Prices have fallen dramatically (over 80% in the last decade!)

But Solar isn't perfect. Solar struggles when:
- The sun goes down (obviously!)
- Clouds roll in unexpectedly
- Space is limited in dense urban areas
- Initial installation costs seem high to homeowners
- Manufacturing the panels requires some rare materials

## Wind's Wonderful Ways
Wind, on the other hand, captures the power of moving air. Wind's strengths include:
- Extremely low cost of electricity production
- Can generate power day and night
- Takes up little ground space (though lots of air space!)
- Uses simple technology with less rare materials
- Scales very effectively for large installations

But Wind faces challenges too:
- Produces variable power based on weather conditions
- Creates some noise that neighbors might notice
- Can impact bird and bat populations
- Requires specific locations with consistent wind
- Visual impact on landscapes that some find unappealing

## How Policies Help Our Friends

Governments around the world have created special rules to help Solar and Wind succeed:

**Investment Tax Credits (ITCs)** act like a discount coupon for building new solar or wind farms, making them much cheaper to construct.

**Production Tax Credits (PTCs)** are like getting a bonus payment for every unit of clean electricity produced, helping wind especially.

**Renewable Portfolio Standards (RPS)** are like promises that states make to use more renewable energy each year, creating a guaranteed market.

**Feed-in Tariffs** guarantee that Solar and Wind get paid a fair price for their electricity, even when competing with older, established power plants.

**Net Metering** allows homeowners with solar panels to sell extra electricity back to the grid, turning meters backward and reducing bills.

**Research Funding** helps scientists discover ways to make Solar and Wind even better and more affordable in the future.

The most successful countries have created a mix of these policies, helping both Solar and Wind contribute to a cleaner energy future. They work best together anyway - Solar shining during the day while Wind often blows strongest at night!

Would you like to hear more about how these renewable friends might power your own home, or about other renewable energy sources like their cousins Hydro and Geothermal?
```



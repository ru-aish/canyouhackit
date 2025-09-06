# AI-Powered Team Matching System - Rating Plan

## Overview
This document outlines the comprehensive AI scoring system for our enhanced team matching platform. We're replacing generic GitHub/Resume scoring with intelligent, category-specific AI that understands gaming team chemistry and ICPC algorithmic complementarity.

## System Architecture

### Current System Analysis
- **Existing Endpoint**: `/api/team-candidates` (hackathon-focused)
- **Current Algorithm**: `complementaryScore = (direct_complements × 3) + (unique_skills × 1) - (overlap_penalty × 0.5)`
- **Current Scale**: 0-1000 unified compatibility scoring
- **Current Data**: GitHub profiles, resumes, basic skills

### Enhanced System Design

#### Core Principle: Category-Specific Intelligence
Replace generic scoring with specialized AI algorithms that understand:
- **Gaming Teams**: Rank compatibility, role synergy, KD ratios, team chemistry
- **ICPC Teams**: Contest ratings, algorithmic strengths, technical complementarity
- **Hackathon Teams**: Current system with enhanced skills matching

## New Data Collection Strategy

### Gaming Teams - Enhanced Form Fields
**Current Fields**: Team name, description, skills required, contact info
**New Strategic Fields**:
1. **Game Rank/Rating** (replacing Practice Schedule)
   - Valorant: Iron, Bronze, Silver, Gold, Platinum, Diamond, Immortal, Radiant
   - CS2: Silver, Gold, MG, DMG, LE, LEM, SMFC, GE
   - Other games: Equivalent ranking systems
2. **KD Ratio**: Numerical input (0.5 - 3.0+ range)
3. **Primary Role**: Entry Fragger, Support, IGL (In-Game Leader), Lurker, AWPer
4. **Secondary Role**: Backup role preference

### ICPC Teams - Enhanced Form Fields
**Current Fields**: Team name, description, programming languages, contact info
**New Strategic Fields**:
1. **Contest Ratings**:
   - Codeforces Rating: 0-4000+ range
   - LeetCode Rating: 0-3500+ range
   - Previous Contest Experience: 0-50+ contests
2. **Algorithmic Strengths**: DP, Graphs, Greedy, Math, Geometry, Strings, Data Structures
3. **Contest Frequency**: Weekly, Bi-weekly, Monthly, Occasional
4. **Team Goals**: World Finals, Regional, Learning, Practice

### Team Application Forms - Enhanced Fields
**Gaming Applications**:
- Gaming Handle/Username
- Current Rank + KD Ratio
- Preferred Role + Backup Role
- Available Gaming Hours per Week
- Communication Style: Aggressive Calls, Strategic, Supportive, Silent

**ICPC Applications**:
- Codeforces/LeetCode Handles
- Contest Ratings + Recent Performance
- Strongest Algorithmic Areas (3-4 selections)
- Contest Participation Frequency
- Learning Goals + Commitment Level

## AI Scoring Algorithms

### Gaming AI Scoring System (prompt1)

#### Input Data Structure
```json
{
  "team_data": {
    "required_rank_range": "Gold-Platinum",
    "primary_role": "IGL",
    "secondary_role": "Support",
    "team_kd_target": "1.2+",
    "communication_style": "Strategic",
    "gaming_hours": "20-30/week"
  },
  "applicant_data": {
    "current_rank": "Gold 3",
    "kd_ratio": 1.35,
    "primary_role": "Entry Fragger",
    "secondary_role": "Lurker",
    "communication_style": "Aggressive Calls",
    "gaming_hours": "25/week"
  }
}
```

#### Scoring Components (Total: 1000 points)
1. **Rank Compatibility (400 points)**:
   - Same rank tier: 350-400 points
   - One tier difference: 250-349 points
   - Two tier difference: 100-249 points
   - Three+ tier difference: 0-99 points

2. **Role Synergy (300 points)**:
   - Perfect complement (IGL + Fragger): 280-300 points
   - Good complement (Support + AWPer): 200-279 points
   - Neutral compatibility: 100-199 points
   - Role conflict: 0-99 points

3. **Performance Metrics (200 points)**:
   - KD ratio alignment with team needs
   - Consistent gaming hours overlap
   - Communication style compatibility

4. **Team Chemistry (100 points)**:
   - Playstyle compatibility analysis
   - Experience level matching
   - Commitment level alignment

#### Gaming Role Compatibility Matrix
```
IGL (In-Game Leader) ↔ Entry Fragger (High Synergy: 300 points)
IGL ↔ Support (Medium Synergy: 250 points)
Support ↔ AWPer (High Synergy: 290 points)
Entry Fragger ↔ Lurker (Medium Synergy: 240 points)
AWPer ↔ Support (High Synergy: 285 points)
```

### ICPC AI Scoring System (prompt2)

#### Input Data Structure
```json
{
  "team_data": {
    "target_cf_rating": "1400-1800",
    "required_strengths": ["DP", "Graphs", "Math"],
    "contest_frequency": "Weekly",
    "team_goal": "Regional Finals",
    "experience_level": "Intermediate"
  },
  "applicant_data": {
    "cf_rating": 1650,
    "lc_rating": 2100,
    "strengths": ["DP", "Greedy", "Data Structures"],
    "contest_frequency": "Bi-weekly",
    "recent_contests": 15,
    "team_goal": "World Finals"
  }
}
```

#### Scoring Components (Total: 1000 points)
1. **Technical Rating Compatibility (400 points)**:
   - CF/LC rating within team range: 350-400 points
   - Slightly above/below range: 250-349 points
   - Significantly different: 100-249 points
   - Major skill gap: 0-99 points

2. **Algorithmic Complementarity (300 points)**:
   - Perfect complement (DP team needs Graphs expert): 280-300 points
   - Good complement (Math + Data Structures): 200-279 points
   - Some overlap with new strengths: 100-199 points
   - Complete overlap: 0-99 points

3. **Contest Engagement (200 points)**:
   - Practice frequency alignment
   - Recent contest participation
   - Consistency in problem-solving

4. **Goal Alignment (100 points)**:
   - Team goal compatibility
   - Commitment level matching
   - Learning objective alignment

#### ICPC Algorithmic Complementarity Matrix
```
DP (Dynamic Programming) ↔ Graph Theory (High Synergy: 300 points)
Math ↔ Geometry (High Synergy: 295 points)
Greedy ↔ Data Structures (Medium Synergy: 250 points)
Strings ↔ DP (Medium Synergy: 240 points)
Math ↔ Number Theory (High Synergy: 290 points)
```

## API Architecture Enhancement

### New Endpoints Structure

#### 1. Gaming Team Matching
**Endpoint**: `/api/gaming-team-candidates`
**Method**: POST
**Input**:
```json
{
  "team_id": 123,
  "category": "gaming",
  "game_type": "valorant", // valorant, cs2, apex, etc.
  "max_candidates": 20
}
```

#### 2. ICPC Team Matching  
**Endpoint**: `/api/icpc-team-candidates`
**Method**: POST
**Input**:
```json
{
  "team_id": 456,
  "category": "icpc",
  "contest_type": "acm", // acm, ioi, local
  "max_candidates": 15
}
```

#### 3. Enhanced Hackathon Matching
**Endpoint**: `/api/hackathon-team-candidates` (existing, enhanced)
**Method**: POST
**Additional**: Enhanced with better skill complementarity

### API Response Format
```json
{
  "status": "success",
  "candidates": [
    {
      "user_id": 789,
      "compatibility_score": 847,
      "breakdown": {
        "rank_compatibility": 380,
        "role_synergy": 295,
        "performance_metrics": 172,
        "team_chemistry": 85
      },
      "reasoning": [
        "Perfect rank match (Gold 3 ↔ Gold 2-Platinum 1 range)",
        "Excellent role synergy (Entry Fragger complements IGL leadership)",
        "Strong KD ratio (1.35) meets team performance standards",
        "Good gaming schedule overlap (25hrs/week fits 20-30hr target)"
      ],
      "user_profile": {
        "name": "Player123",
        "current_rank": "Gold 3",
        "kd_ratio": 1.35,
        "primary_role": "Entry Fragger",
        "gaming_hours": "25/week"
      }
    }
  ],
  "total_candidates": 1,
  "processing_time": "1.2s"
}
```

## Prompt Templates

### Gaming AI Prompt (prompt1.txt)
```
You are an expert eSports team analyst and gaming coach specializing in team chemistry and performance optimization. Analyze the compatibility between a gaming team's requirements and a potential applicant.

**IMPORTANT: Use precise, non-round scores like 347, 628, 754, 891, 573, etc. Avoid scores ending in 0 or 5.**

**IMPORTANT: Respond ONLY in valid JSON format with this exact structure:**

{
  "compatibility_score": 628,
  "breakdown": {
    "rank_compatibility": 380,
    "role_synergy": 195,
    "performance_metrics": 142,
    "team_chemistry": 78
  },
  "reasoning": [
    "Specific analysis of rank compatibility with examples",
    "Detailed role synergy assessment with tactical reasoning",
    "Performance metrics evaluation including KD ratio analysis",
    "Team chemistry assessment based on communication and playstyle"
  ]
}

**Scoring Components (Total: 1000 points):**
1. **Rank Compatibility (0-400)**: Evaluate rank/rating alignment
2. **Role Synergy (0-300)**: Assess tactical role complementarity  
3. **Performance Metrics (0-200)**: KD ratio, gaming hours, consistency
4. **Team Chemistry (0-100)**: Communication style, playstyle fit

**Role Synergy Matrix:**
- IGL + Entry Fragger = High Synergy (280-300)
- Support + AWPer = High Synergy (285-300)
- IGL + Support = Medium Synergy (220-250)
- Entry Fragger + Lurker = Medium Synergy (200-240)

**Respond with valid JSON only - no additional text or explanations.**
```

### ICPC AI Prompt (prompt2.txt)
```
You are an expert competitive programming coach and algorithmic problem-solving specialist. Analyze the compatibility between an ICPC team's requirements and a potential applicant based on technical skills and algorithmic complementarity.

**IMPORTANT: Use precise, non-round scores like 347, 628, 754, 891, 573, etc. Avoid scores ending in 0 or 5.**

**IMPORTANT: Respond ONLY in valid JSON format with this exact structure:**

{
  "compatibility_score": 742,
  "breakdown": {
    "rating_compatibility": 345,
    "algorithmic_complementarity": 268,
    "contest_engagement": 162,
    "goal_alignment": 89
  },
  "reasoning": [
    "Detailed rating compatibility analysis with CF/LC scores",
    "Algorithmic strength complementarity assessment",
    "Contest frequency and engagement evaluation",
    "Team goal and commitment level alignment analysis"
  ]
}

**Scoring Components (Total: 1000 points):**
1. **Rating Compatibility (0-400)**: CF/LC rating alignment with team range
2. **Algorithmic Complementarity (0-300)**: Skill gap filling and strengths balance
3. **Contest Engagement (0-200)**: Practice frequency, recent participation
4. **Goal Alignment (0-100)**: Team objectives and commitment matching

**Algorithmic Complementarity Matrix:**
- DP + Graph Theory = High Synergy (280-300)
- Math + Geometry = High Synergy (290-300)
- Greedy + Data Structures = Medium Synergy (220-250)
- Strings + DP = Medium Synergy (200-240)

**Rating Compatibility Guidelines:**
- Within target range: 350-400 points
- Slightly outside range: 250-349 points  
- Significantly different: 100-249 points
- Major skill gap: 0-99 points

**Respond with valid JSON only - no additional text or explanations.**
```

## Database Schema Updates

### Enhanced Team Tables

#### gaming_teams (new table)
```sql
CREATE TABLE gaming_teams (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    team_name TEXT NOT NULL,
    game_type TEXT NOT NULL, -- valorant, cs2, apex, etc.
    required_rank_min TEXT,
    required_rank_max TEXT,
    primary_role_needed TEXT,
    secondary_role_needed TEXT,
    target_kd_ratio REAL,
    gaming_hours_min INTEGER,
    gaming_hours_max INTEGER,
    communication_style TEXT,
    team_description TEXT,
    creator_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (creator_id) REFERENCES users(id)
);
```

#### icpc_teams (new table)
```sql
CREATE TABLE icpc_teams (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    team_name TEXT NOT NULL,
    contest_type TEXT DEFAULT 'acm', -- acm, ioi, local
    cf_rating_min INTEGER,
    cf_rating_max INTEGER,
    required_strengths TEXT, -- JSON array of algorithmic areas
    contest_frequency TEXT,
    team_goal TEXT,
    experience_level TEXT,
    team_description TEXT,
    creator_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (creator_id) REFERENCES users(id)
);
```

### Enhanced Application Tables

#### gaming_applications (new table)
```sql
CREATE TABLE gaming_applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    team_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    gaming_handle TEXT,
    current_rank TEXT,
    kd_ratio REAL,
    primary_role TEXT,
    secondary_role TEXT,
    gaming_hours_per_week INTEGER,
    communication_style TEXT,
    experience_description TEXT,
    application_status TEXT DEFAULT 'pending',
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (team_id) REFERENCES gaming_teams(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

#### icpc_applications (new table)
```sql
CREATE TABLE icpc_applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    team_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    codeforces_handle TEXT,
    codeforces_rating INTEGER,
    leetcode_handle TEXT,
    leetcode_rating INTEGER,
    algorithmic_strengths TEXT, -- JSON array
    contest_frequency TEXT,
    recent_contests INTEGER,
    team_goals TEXT,
    commitment_level TEXT,
    application_status TEXT DEFAULT 'pending',
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (team_id) REFERENCES icpc_teams(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

## Implementation Phases

### Phase 1: Data Collection Enhancement
1. **Update Form Fields**: Add rank, KD ratio, roles for gaming; add CF/LC ratings, strengths for ICPC
2. **Database Schema**: Create new tables for gaming and ICPC teams/applications
3. **Form Validation**: Implement client-side and server-side validation for new fields

### Phase 2: AI Prompt Development
1. **Create prompt1.txt**: Gaming-specific AI scoring prompt
2. **Create prompt2.txt**: ICPC-specific AI scoring prompt  
3. **Test Prompts**: Validate with sample data and refine algorithms

### Phase 3: API Development
1. **New Rating Services**: Separate classes for GamingRatingService and ICPCRatingService
2. **New Endpoints**: Implement `/api/gaming-team-candidates` and `/api/icpc-team-candidates`
3. **Enhanced Scoring**: Integrate specialized prompts with new data fields

### Phase 4: Frontend Integration
1. **Separate Find People Pages**: Create dedicated pages for gaming and ICPC team search
2. **Enhanced Filters**: Add category-specific filtering (rank ranges, algorithmic strengths)
3. **Improved UI**: Show compatibility breakdowns and reasoning in results

### Phase 5: Testing & Optimization
1. **Algorithm Tuning**: Refine scoring weights based on real-world feedback
2. **Performance Testing**: Ensure API response times under 2 seconds
3. **User Testing**: Gather feedback on match quality and relevance

## Success Metrics

### Quantitative Metrics
- **Match Relevance**: >80% of top 5 recommendations rated as "good fit" by teams
- **Response Time**: API responses under 2 seconds for candidate generation
- **User Engagement**: 50%+ increase in team application rates
- **Match Success**: 30%+ increase in successful team formations

### Qualitative Metrics
- **Gaming Teams**: Better rank compatibility, improved role balance, higher team chemistry
- **ICPC Teams**: Stronger algorithmic complementarity, better contest performance correlation
- **User Feedback**: Positive feedback on recommendation relevance and match explanations

## Technical Considerations

### Scalability
- **Caching Strategy**: Cache user profiles and ratings for 24-hour periods
- **Async Processing**: Use background jobs for complex scoring calculations
- **Database Optimization**: Index on frequently queried fields (ratings, ranks, strengths)

### Data Privacy
- **Rating Visibility**: Users can choose to hide specific ratings/ranks
- **Profile Privacy**: Granular control over data sharing with teams
- **Anonymization**: Option for anonymous team applications

### Error Handling
- **Fallback Scoring**: Default compatibility scores when AI fails
- **Graceful Degradation**: Basic matching when enhanced data unavailable
- **User Feedback**: Clear error messages and alternative suggestions

This comprehensive rating plan transforms our team matching system from generic GitHub/Resume analysis to intelligent, category-specific AI that understands the nuances of gaming team chemistry and ICPC algorithmic complementarity, providing users with highly relevant and actionable team recommendations.
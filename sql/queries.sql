-- Q1: Breaches per state (top 10)
SELECT state, COUNT(*) AS breaches
FROM breaches
WHERE state IS NOT NULL
GROUP BY state
ORDER BY breaches DESC
LIMIT 10;

-- Q2: Breach count and total people affected per entity type
SELECT covered_entity_type,
       COUNT(*) AS breaches,
       SUM(individuals_affected) AS total_affected
FROM breaches
WHERE covered_entity_type IS NOT NULL
GROUP BY covered_entity_type
ORDER BY total_affected DESC;

-- Q3: Top 10 largest breaches
SELECT name_of_covered_entity, covered_entity_type, breach_year, individuals_affected
FROM breaches
ORDER BY individuals_affected DESC
LIMIT 10;

-- Q4: Breaches per year
SELECT breach_year, COUNT(*) AS breaches
FROM breaches
GROUP BY breach_year
ORDER BY breach_year;

-- Q5: Breaches by primary breach type
SELECT breach_type_primary, COUNT(*) AS breaches, SUM(individuals_affected) AS total_affected
FROM breaches
WHERE breach_type_primary IS NOT NULL
GROUP BY breach_type_primary
ORDER BY breaches DESC;

-- Q6: Massachusetts breaches by entity type
SELECT covered_entity_type, COUNT(*) AS breaches, SUM(individuals_affected) AS total_affected
FROM breaches
WHERE state = 'MA'
GROUP BY covered_entity_type
ORDER BY breaches DESC;
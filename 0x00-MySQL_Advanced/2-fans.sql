-- Create a temporary table to store the aggregated fan counts per country
CREATE TEMPORARY TABLE temp_fan_counts AS
SELECT origin, COUNT(*) AS nb_fans
FROM metal_bands
GROUP BY origin;

-- Rank the country origins based on the number of fans
SELECT origin, nb_fans
FROM temp_fan_counts
ORDER BY nb_fans DESC;

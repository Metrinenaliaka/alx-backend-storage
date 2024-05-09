-- Create a temporary table to hold the rankings
CREATE TEMPORARY TABLE temp_rankings AS
SELECT origin, COUNT(*) AS nb_fans
FROM metal_bands
GROUP BY origin;

-- Rank the origins based on the number of non-unique fans
SELECT origin, nb_fans,
       DENSE_RANK() OVER (ORDER BY nb_fans DESC) AS ranking
FROM temp_rankings
ORDER BY ranking;

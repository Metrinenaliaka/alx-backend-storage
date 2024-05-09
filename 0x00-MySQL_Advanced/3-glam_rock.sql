-- Create a view to split the formed and split attributes into separate columns
CREATE VIEW band_dates AS
SELECT
    band_name,
    SUBSTRING_INDEX(founded, '-', 1) AS formed_year,
    SUBSTRING_INDEX(founded, '-', -1) AS split_year
FROM metal_bands;

-- Calculate the lifespan in years for each band
CREATE VIEW band_lifespan AS
SELECT
    band_name,
    (2022 - formed_year) AS lifespan
FROM band_dates;

-- List all bands with Glam rock as their main style, ranked by their longevity
SELECT
    b.band_name,
    bl.lifespan
FROM
    metal_bands b
JOIN
    band_lifespan bl ON b.band_name = bl.band_name
WHERE
    b.style LIKE '%Glam rock%'
ORDER BY
    bl.lifespan DESC;

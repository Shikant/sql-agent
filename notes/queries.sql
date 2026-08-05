SELECT
    c.CustomerId,
    c.FirstName,
    c.LastName,
    SUM(i.Total) AS TotalSpent
FROM Customer c
JOIN Invoice i
    ON c.CustomerId = i.CustomerId
GROUP BY
    c.CustomerId,
    c.FirstName,
    c.LastName
ORDER BY TotalSpent DESC
LIMIT 5;

SELECT
    g.Name,
    COUNT(t.TrackId) AS NumberOfTracks
FROM Genre g
JOIN Track t
    ON g.GenreId = t.GenreId
GROUP BY g.Name
ORDER BY NumberOfTracks DESC;

SELECT
    g.Name,
    COUNT(t.TrackId) AS NumberOfTracks
FROM Genre g
JOIN Track t
    ON g.GenreId = t.GenreId
GROUP BY g.Name
ORDER BY NumberOfTracks DESC;

SELECT
    BillingCountry,
    SUM(Total) AS TotalSales
FROM Invoice
GROUP BY BillingCountry
ORDER BY TotalSales DESC;

SELECT
    Name,
    Milliseconds
FROM Track
ORDER BY Milliseconds DESC
LIMIT 5;

SELECT
    c.CustomerId,
    c.FirstName,
    c.LastName,
    COUNT(i.InvoiceId) AS InvoiceCount
FROM Customer c
LEFT JOIN Invoice i
    ON c.CustomerId = i.CustomerId
GROUP BY
    c.CustomerId,
    c.FirstName,
    c.LastName
ORDER BY InvoiceCount DESC;
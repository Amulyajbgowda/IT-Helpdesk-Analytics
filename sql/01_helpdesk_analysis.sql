-- ============================================================
-- IT HELPDESK INTELLIGENCE ANALYSIS
-- Dataset: UCI Incident Management Process Enriched Event Log
-- Database: it_helpdesk_analytics
-- ============================================================


-- ============================================================
-- 1. OVERALL SLA PERFORMANCE
-- ============================================================

SELECT
    sla_status,
    COUNT(*) AS incidents,
    ROUND(
        COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (),
        2
    ) AS percentage,
    ROUND(AVG(resolution_hours), 2) AS avg_resolution_hours
FROM incidents
GROUP BY sla_status
ORDER BY incidents DESC;


-- ============================================================
-- 2. SLA PERFORMANCE BY PRIORITY
-- ============================================================

SELECT
    priority_label,
    COUNT(*) AS incidents,
    SUM(
        CASE
            WHEN sla_status = 'Breached SLA' THEN 1
            ELSE 0
        END
    ) AS sla_breaches,
    ROUND(
        SUM(
            CASE
                WHEN sla_status = 'Breached SLA' THEN 1
                ELSE 0
            END
        ) * 100.0 / COUNT(*),
        2
    ) AS sla_breach_rate,
    ROUND(AVG(resolution_hours), 2) AS avg_resolution_hours
FROM incidents
GROUP BY priority_label
ORDER BY sla_breach_rate DESC;


-- ============================================================
-- 3. SLA PERFORMANCE BY ASSIGNMENT GROUP
-- Only groups with at least 100 incidents are considered.
-- ============================================================

SELECT
    assignment_group,
    COUNT(*) AS incidents,
    SUM(
        CASE
            WHEN sla_status = 'Breached SLA' THEN 1
            ELSE 0
        END
    ) AS sla_breaches,
    ROUND(
        SUM(
            CASE
                WHEN sla_status = 'Breached SLA' THEN 1
                ELSE 0
            END
        ) * 100.0 / COUNT(*),
        2
    ) AS sla_breach_rate,
    ROUND(AVG(resolution_hours), 2) AS avg_resolution_hours
FROM incidents
GROUP BY assignment_group
HAVING COUNT(*) >= 100
ORDER BY sla_breach_rate DESC;


-- ============================================================
-- 4. SLA PERFORMANCE BY INCIDENT CATEGORY
-- Only categories with at least 100 incidents are considered.
-- ============================================================

SELECT
    category,
    COUNT(*) AS incidents,
    SUM(
        CASE
            WHEN sla_status = 'Breached SLA' THEN 1
            ELSE 0
        END
    ) AS sla_breaches,
    ROUND(
        SUM(
            CASE
                WHEN sla_status = 'Breached SLA' THEN 1
                ELSE 0
            END
        ) * 100.0 / COUNT(*),
        2
    ) AS sla_breach_rate,
    ROUND(AVG(resolution_hours), 2) AS avg_resolution_hours
FROM incidents
GROUP BY category
HAVING COUNT(*) >= 100
ORDER BY sla_breach_rate DESC;


-- ============================================================
-- 5. REASSIGNMENT VS SLA PERFORMANCE
-- ============================================================

SELECT
    CASE
        WHEN reassignment_count >= 3 THEN 'High Reassignment'
        ELSE 'Low Reassignment'
    END AS reassignment_group,
    COUNT(*) AS incidents,
    SUM(
        CASE
            WHEN sla_status = 'Breached SLA' THEN 1
            ELSE 0
        END
    ) AS sla_breaches,
    ROUND(
        SUM(
            CASE
                WHEN sla_status = 'Breached SLA' THEN 1
                ELSE 0
            END
        ) * 100.0 / COUNT(*),
        2
    ) AS sla_breach_rate,
    ROUND(AVG(resolution_hours), 2) AS avg_resolution_hours
FROM incidents
GROUP BY
    CASE
        WHEN reassignment_count >= 3 THEN 'High Reassignment'
        ELSE 'Low Reassignment'
    END
ORDER BY sla_breach_rate DESC;


-- ============================================================
-- 6. REOPENED INCIDENTS VS SLA PERFORMANCE
-- ============================================================

SELECT
    CASE
        WHEN was_reopened = TRUE THEN 'Reopened'
        ELSE 'Not Reopened'
    END AS reopen_group,
    COUNT(*) AS incidents,
    SUM(
        CASE
            WHEN sla_status = 'Breached SLA' THEN 1
            ELSE 0
        END
    ) AS sla_breaches,
    ROUND(
        SUM(
            CASE
                WHEN sla_status = 'Breached SLA' THEN 1
                ELSE 0
            END
        ) * 100.0 / COUNT(*),
        2
    ) AS sla_breach_rate,
    ROUND(AVG(resolution_hours), 2) AS avg_resolution_hours
FROM incidents
GROUP BY
    CASE
        WHEN was_reopened = TRUE THEN 'Reopened'
        ELSE 'Not Reopened'
    END
ORDER BY sla_breach_rate DESC;


-- ============================================================
-- 7. MONTHLY SLA TREND
-- ============================================================

SELECT
    opened_month_year,
    COUNT(*) AS incidents,
    SUM(
        CASE
            WHEN sla_status = 'Breached SLA' THEN 1
            ELSE 0
        END
    ) AS sla_breaches,
    ROUND(
        SUM(
            CASE
                WHEN sla_status = 'Breached SLA' THEN 1
                ELSE 0
            END
        ) * 100.0 / COUNT(*),
        2
    ) AS sla_breach_rate
FROM incidents
GROUP BY opened_month_year
ORDER BY opened_month_year;


-- ============================================================
-- 8. INCIDENT RESOLUTION TIME DISTRIBUTION
-- ============================================================

SELECT
    resolution_bucket,
    COUNT(*) AS incidents,
    ROUND(
        COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (),
        2
    ) AS percentage
FROM incidents
GROUP BY resolution_bucket
ORDER BY incidents DESC;
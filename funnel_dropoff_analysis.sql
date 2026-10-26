-- =====================================================================
-- SAAS PRODUCT ACTIVATION FUNNEL & STEP CONVERSION
-- Author: Puneet Goswami
-- Description: Analyzes milestone drop-offs from initial signup to paid tier.
-- =====================================================================

WITH user_event_milestones AS (
    SELECT 
        user_id,
        account_id,
        signup_channel,
        created_at,
        MAX(CASE WHEN event_name = 'user_signup' THEN event_timestamp END) AS signup_time,
        MAX(CASE WHEN event_name = 'workspace_created' THEN event_timestamp END) AS workspace_time,
        MAX(CASE WHEN event_name = 'team_member_invited' THEN event_timestamp END) AS invite_time,
        MAX(CASE WHEN event_name = 'first_core_action' THEN event_timestamp END) AS activation_time,
        MAX(CASE WHEN event_name = 'paid_subscription_started' THEN event_timestamp END) AS conversion_time
    FROM product_analytics.events
    WHERE event_timestamp >= CURRENT_DATE - INTERVAL '90 DAYS'
    GROUP BY user_id, account_id, signup_channel, created_at
),

funnel_stages AS (
    SELECT 
        signup_channel,
        COUNT(DISTINCT user_id) AS total_signups,
        COUNT(DISTINCT CASE WHEN workspace_time IS NOT NULL THEN user_id END) AS step_1_workspace,
        COUNT(DISTINCT CASE WHEN invite_time IS NOT NULL THEN user_id END) AS step_2_invited_team,
        COUNT(DISTINCT CASE WHEN activation_time IS NOT NULL THEN user_id END) AS step_3_activated,
        COUNT(DISTINCT CASE WHEN conversion_time IS NOT NULL THEN user_id END) AS step_4_paid_conversion
    FROM user_event_milestones
    GROUP BY signup_channel
)

SELECT 
    signup_channel,
    total_signups,
    step_1_workspace,
    ROUND((step_1_workspace * 100.0) / total_signups, 2) AS pct_workspace_created,
    step_2_invited_team,
    ROUND((step_2_invited_team * 100.0) / step_1_workspace, 2) AS pct_team_invite_rate,
    step_3_activated,
    ROUND((step_3_activated * 100.0) / step_2_invited_team, 2) AS pct_core_activation_rate,
    step_4_paid_conversion,
    ROUND((step_4_paid_conversion * 100.0) / total_signups, 2) AS overall_visitor_to_paid_rate
FROM funnel_stages
ORDER BY total_signups DESC;
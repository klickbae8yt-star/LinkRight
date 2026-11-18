# Performance Data Schema

The contract for `posts.csv`. The Strategist and the System Optimizer read it. MVP, the owner fills it by hand, one row per published post. Later a Tampermonkey passive collector appends to the same schema, so nothing downstream changes.

## Columns

- post_date, the date published, YYYY-MM-DD
- day_number, the calendar day, for example 7
- post_type, from post-types.md
- pillar, the positioning pillar it served
- media_type, image, document carousel, video, poll, text
- topic, a short label
- hook, the opening line used
- impressions
- reactions
- comments
- shares
- saves
- profile_views
- follower_delta, change in followers attributable to the post
- dwell_estimate, if available, otherwise blank
- inbound, recruiter or hiring manager messages this post drove
- notes, anything worth remembering

## Rules

One row per post. Keep the labels consistent so the Strategist can dedupe and the Optimizer can group. Leave a cell blank rather than guessing. The real numbers always override the general rules in the engine knowledge.

#!/usr/bin/env python3
"""
Candidate Evaluator — scores candidates against all 14 job roles.
Processes candidates from both all_resumes.md and #ApplyToAmex - Form Responses 1.csv.
Outputs a single CSV with candidate details + 14 score columns.
"""

import re
import os
import csv
import pandas as pd

RESUMES_FILE = '/Users/satvikjain/Downloads/Navii Jobs/data/all_resumes.md'
AMEX_FILE = '/Users/satvikjain/Downloads/Navii Jobs/data/#ApplyToAmex - Form Responses 1.csv'
OUTPUT_FILE = '/Users/satvikjain/Downloads/Navii Jobs/output/evaluation_results.csv'

ROLES = [
    {'id': 1, 'col': '1_iFIT_SWE', 'title': 'Senior SWE Data Services', 'company': 'iFIT', 'location': 'Remote US',
     'pillars': [
         {'weight': 25, 'keywords': ['streaming', 'kafka', 'kinesis', 'event-driven', 'pipeline', 'ingestion', 'time-series', 'telemetry', 'real-time', 'data pipeline', 'msk', 'event processing', 'message queue', 'pubsub']},
         {'weight': 20, 'keywords': ['nodejs', 'node.js', 'typescript', 'aws', 'lambda', 'ecs', 'rds', 's3', 'terraform', 'serverless', 'api', 'rest', 'graphql', 'microservices', 'cloud', 'docker', 'kubernetes']},
         {'weight': 15, 'keywords': ['ai', 'llm', 'machine learning', 'ml', 'copilot', 'cursor', 'langchain', 'llamaindex', 'ai tool', 'automation', 'gpt', 'openai', 'claude']},
         {'weight': 10, 'keywords': ['fitness', 'health', 'iot', 'mqtt', 'wearable', 'strava', 'garmin', 'sensor', 'healthcare', 'connected device']},
         {'weight': 10, 'keywords': ['slo', 'observability', 'monitoring', 'incident', 'postmortem', 'reliability', 'schema', 'versioning', 'alerting', 'logging', 'traces', 'metrics']},
         {'weight': 20, 'keywords': ['remote', 'async', 'distributed team', 'self-starter', 'independent', 'us timezone', 'pacific', 'eastern']}
     ]},
    {'id': 2, 'col': '2_Arbor_Senior', 'title': 'Senior Founding SWE Backend', 'company': 'Arbor AI', 'location': 'SF Bay Area',
     'pillars': [
         {'weight': 25, 'keywords': ['low-latency', 'latency', 'high-qps', 'qps', 'throughput', 'performance', 'serving', 'auction', 'ranking', 'real-time', 'p99', 'millisecond']},
         {'weight': 20, 'keywords': ['distributed', 'microservices', 'backend', 'systems', 'scalability', 'production', 'debugging', 'end-to-end', 'infrastructure']},
         {'weight': 15, 'keywords': ['attribution', 'experimentation', 'a/b testing', 'incrementality', 'reporting', 'measurement', 'analytics', 'metrics']},
         {'weight': 15, 'keywords': ['founding', 'early employee', 'startup', 'first 10', 'technical direction', 'engineering culture', 'hiring', 'founder']},
         {'weight': 10, 'keywords': ['ads', 'ad serving', 'monetization', 'targeting', 'campaign', 'rtb', 'real-time bidding', 'marketplace', 'decisioning']},
         {'weight': 15, 'keywords': ['bay area', 'san francisco', 'sf', 'palo alto', 'california', 'bay', 'in-office']}
     ]},
    {'id': 3, 'col': '3_Arbor_Founding', 'title': 'Founding AI-Accelerated SWE', 'company': 'Arbor AI', 'location': 'SF Bay Area',
     'pillars': [
         {'weight': 25, 'keywords': ['low-latency', 'latency', 'performance', 'high-qps', 'throughput', 'optimization', 'serving', 'real-time', 'speed']},
         {'weight': 20, 'keywords': ['distributed', 'backend', 'production', 'services', 'systems', 'debugging', 'engineering', 'end-to-end', 'scalability']},
         {'weight': 15, 'keywords': ['ai', 'cursor', 'copilot', 'claude', 'ai tool', 'ai-augmented', 'llm', 'ai agent', 'automation']},
         {'weight': 15, 'keywords': ['startup', 'founding', 'ambiguity', 'early stage', 'ownership', 'self-directed', 'uncertainty']},
         {'weight': 10, 'keywords': ['ads', 'monetization', 'targeting', 'campaign', 'marketplace', 'auction', 'rtb']},
         {'weight': 15, 'keywords': ['bay area', 'san francisco', 'sf', 'palo alto', 'california', 'in-office']}
     ]},
    {'id': 4, 'col': '4_Ciphus_Java', 'title': 'Senior Java Backend Engineer', 'company': 'Ciphus', 'location': 'Remote India',
     'pillars': [
         {'weight': 25, 'keywords': ['java', 'jdk', 'maven', 'spring', 'gradle', 'jvm', 'junit', 'java 17', 'java 21', 'toolchain', 'build']},
         {'weight': 20, 'keywords': ['tdd', 'test-driven', 'testing', 'unit test', 'integration test', 'quality', 'regression', 'test coverage']},
         {'weight': 15, 'keywords': ['observability', 'monitoring', 'logs', 'metrics', 'traces', 'alerting', 'debugging', 'incident', 'production']},
         {'weight': 10, 'keywords': ['ci/cd', 'pipeline', 'git', 'github actions', 'jenkins', 'devops', 'cloud', 'aws', 'automation']},
         {'weight': 10, 'keywords': ['ai', 'enterprise', 'platform', 'vector database', 'data governance', 'privacy', 'compliance', 'security']},
         {'weight': 20, 'keywords': ['hyderabad', 'india', 'bangalore', 'bengaluru', 'remote india', 'south india', 'telangana', 'pune', 'mumbai']}
     ]},
    {'id': 5, 'col': '5_Key_Product', 'title': 'Product Engineer Core', 'company': 'Key', 'location': 'Palo Alto',
     'pillars': [
         {'weight': 25, 'keywords': ['full-stack', 'fullstack', 'frontend', 'backend', 'react', 'nextjs', 'next.js', 'nodejs', 'shipped', 'production', 'startup', 'end-to-end']},
         {'weight': 20, 'keywords': ['user', 'feedback', 'product', 'customer', 'empathy', 'ux', 'user experience', 'iteration', 'design']},
         {'weight': 20, 'keywords': ['startup', 'ambiguity', 'fast-paced', 'fast moving', 'iteration', 'on-call', 'context switching', 'ownership']},
         {'weight': 10, 'keywords': ['ai', 'llm', 'ai-enabled', 'machine learning', 'inference', 'gpt', 'openai', 'ai product']},
         {'weight': 10, 'keywords': ['mentor', 'code review', 'pairing', 'tech talk', 'onboarding', 'team', 'leadership']},
         {'weight': 15, 'keywords': ['palo alto', 'bay area', 'san francisco', 'sf', 'california', 'in-office', 'bay']}
     ]},
    {'id': 6, 'col': '6_Vinyl_SPM_Transfer', 'title': 'Senior PM Transfer Agent DTC/DRS', 'company': 'Vinyl Equity', 'location': 'Mangaluru',
     'pillars': [
         {'weight': 25, 'keywords': ['regulatory', 'compliance', 'governance', 'audit', 'sec', 'dtc', 'drs', 'settlement', 'regulated', 'fintech', 'capital markets']},
         {'weight': 20, 'keywords': ['dtc', 'drs', 'corporate actions', 'transfer agent', 'securities', 'equity', 'settlement', 'clearing', 'stock', 'dividend']},
         {'weight': 15, 'keywords': ['cross-functional', 'stakeholder', 'legal', 'ops', 'product manager', 'pm', 'product management', 'requirements']},
         {'weight': 15, 'keywords': ['state machine', 'failure mode', 'edge case', 'error handling', 'diagnostics', 'system behavior', 'workflow']},
         {'weight': 10, 'keywords': ['self-serve', 'automation', 'workflow', 'platform', 'api', 'integration']},
         {'weight': 15, 'keywords': ['mangaluru', 'mangalore', 'india', 'south india', 'karnataka', 'kerala', 'udupi', 'nitk', 'manipal']}
     ]},
    {'id': 7, 'col': '7_Vinyl_PM_Issuer', 'title': 'Product Manager Issuer Activation', 'company': 'Vinyl Equity', 'location': 'Chicago',
     'pillars': [
         {'weight': 25, 'keywords': ['self-service', 'self-serve', 'product', 'platform', 'saas', 'user experience', 'onboarding', 'activation']},
         {'weight': 20, 'keywords': ['data migration', 'api', 'technical', 'integration', 'etl', 'data pipeline', 'system integration']},
         {'weight': 15, 'keywords': ['cross-functional', 'collaboration', 'communication', 'stakeholder', 'alignment', 'product manager']},
         {'weight': 15, 'keywords': ['sandbox', 'pre-sales', 'post-sales', 'demo', 'proof of concept', 'poc', 'customer success']},
         {'weight': 10, 'keywords': ['ai', 'ml', 'machine learning', 'data-driven', 'analytics', 'insights']},
         {'weight': 15, 'keywords': ['chicago', 'illinois', 'midwest', 'us', 'on-site', 'in-office']}
     ]},
    {'id': 8, 'col': '8_Vinyl_SPM_Payment', 'title': 'Senior PM Payment Solutions', 'company': 'Vinyl Equity', 'location': 'Chicago',
     'pillars': [
         {'weight': 25, 'keywords': ['payment', 'payments', 'fintech', 'stablecoin', 'cross-border', 'wire', 'ach', 'faster payments', 'b2b payments']},
         {'weight': 20, 'keywords': ['stablecoin', 'crypto', 'blockchain', 'multi-rail', 'payment rail', 'defi', 'usdc', 'usdt']},
         {'weight': 15, 'keywords': ['regulatory', 'compliance', 'aml', 'kyc', 'regulation', 'licensing', 'audit']},
         {'weight': 15, 'keywords': ['sales', 'vendor', 'partnership', 'bd', 'business development', 'negotiation', 'deal']},
         {'weight': 10, 'keywords': ['metrics', 'kpi', 'operational', 'efficiency', 'process', 'automation', 'monitoring']},
         {'weight': 15, 'keywords': ['chicago', 'illinois', 'midwest', 'us', 'hybrid', 'in-office']}
     ]},
    {'id': 9, 'col': '9_Vinyl_Production', 'title': 'Production Engineer', 'company': 'Vinyl Equity', 'location': 'Mangaluru',
     'pillars': [
         {'weight': 25, 'keywords': ['production', 'reliability', 'sre', 'devops', 'incident', 'on-call', 'uptime', 'availability', 'slo', 'sli', 'sla']},
         {'weight': 20, 'keywords': ['debugging', 'incident', 'root cause', 'postmortem', 'troubleshooting', 'firefighting', 'diagnostics']},
         {'weight': 20, 'keywords': ['observability', 'monitoring', 'datadog', 'grafana', 'prometheus', 'logging', 'metrics', 'traces', 'alerting']},
         {'weight': 15, 'keywords': ['us timezone', 'pacific', 'eastern', 'night shift', 'us hours', 'us market']},
         {'weight': 10, 'keywords': ['capital markets', 'fintech', 'trading', 'settlement', 'clearing', 'exchange', 'financial']},
         {'weight': 10, 'keywords': ['mangaluru', 'mangalore', 'india', 'karnataka', 'south india', 'nitk', 'manipal', 'udupi']}
     ]},
    {'id': 10, 'col': '10_Vinyl_AI_Lead', 'title': 'Applied AI Lead', 'company': 'Vinyl Equity', 'location': 'Mangaluru',
     'pillars': [
         {'weight': 25, 'keywords': ['ai', 'llm', 'langchain', 'llamaindex', 'mcp', 'agent', 'multi-agent', 'vector', 'embedding', 'n8n', 'zapier', 'automation', 'gpt', 'openai', 'claude', 'rag']},
         {'weight': 20, 'keywords': ['nodejs', 'node.js', 'nextjs', 'react', 'aws', 'typescript', 'javascript', 'ci/cd', 'github', 'api']},
         {'weight': 15, 'keywords': ['senior', 'lead', 'manager', 'playbook', 'training', 'cross-functional', 'organizational', 'staff engineer', 'engineering manager']},
         {'weight': 10, 'keywords': ['fintech', 'regtech', 'compliance', 'cap table', 'securities', 'wealthtech', 'financial', 'audit']},
         {'weight': 10, 'keywords': ['velocity', 'automation', 'developer productivity', 'build vs buy', 'low-code', 'open source', 'efficiency']},
         {'weight': 20, 'keywords': ['mangaluru', 'mangalore', 'nitk', 'manipal', 'udupi', 'karnataka', 'kerala', 'south india', 'bangalore', 'bengaluru']}
     ]},
    {'id': 11, 'col': '11_Vinyl_Fullstack', 'title': 'Full-stack Engineer', 'company': 'Vinyl Equity', 'location': 'Mangaluru',
     'pillars': [
         {'weight': 25, 'keywords': ['nodejs', 'node.js', 'typescript', 'api', 'rest', 'graphql', 'express', 'nestjs', 'fastify', 'backend']},
         {'weight': 20, 'keywords': ['react', 'nextjs', 'next.js', 'frontend', 'full-stack', 'fullstack', 'css', 'tailwind', 'ui']},
         {'weight': 15, 'keywords': ['aws', 'cloud', 'docker', 'kubernetes', 'terraform', 'ci/cd', 'deploy', 'devops', 'lambda', 'ecs']},
         {'weight': 10, 'keywords': ['fintech', 'financial', 'payments', 'banking', 'securities', 'compliance', 'audit']},
         {'weight': 10, 'keywords': ['code review', 'collaboration', 'team', 'git', 'pull request', 'pairing', 'mentor']},
         {'weight': 20, 'keywords': ['mangaluru', 'mangalore', 'nitk', 'manipal', 'udupi', 'karnataka', 'kerala', 'south india', 'bangalore', 'bengaluru']}
     ]},
    {'id': 12, 'col': '12_Vinyl_Founding_TPM', 'title': 'Founding TPM Tokenization GTM', 'company': 'Vinyl Equity', 'location': 'Chicago',
     'pillars': [
         {'weight': 25, 'keywords': ['product manager', 'gtm', 'go-to-market', 'product management', 'roadmap', 'strategy', 'launch', 'market']},
         {'weight': 20, 'keywords': ['tokenization', 'blockchain', 'web3', 'defi', 'smart contract', 'nft', 'crypto', 'ethereum', 'solana']},
         {'weight': 15, 'keywords': ['cross-functional', 'stakeholder', 'leadership', 'alignment', 'communication', 'product owner']},
         {'weight': 15, 'keywords': ['market research', 'competitive analysis', 'roadmap', 'prioritization', 'user research', 'discovery']},
         {'weight': 10, 'keywords': ['regulatory', 'compliance', 'legal', 'sec', 'regulation', 'audit', 'governance']},
         {'weight': 15, 'keywords': ['chicago', 'illinois', 'midwest', 'us', 'hybrid', 'in-office']}
     ]},
    {'id': 13, 'col': '13_Stratasys_SWE', 'title': 'Senior Software Engineer', 'company': 'Stratasys', 'location': 'Pune',
     'pillars': [
         {'weight': 25, 'keywords': ['react', 'nodejs', 'node.js', 'typescript', 'javascript', 'full-stack', 'nextjs', 'frontend', 'backend']},
         {'weight': 20, 'keywords': ['aws', 'cloud', 'architecture', 'lambda', 's3', 'dynamodb', 'ec2', 'ecs', 'terraform', 'serverless']},
         {'weight': 15, 'keywords': ['iot', 'saas', 'connected', 'device', 'firmware', 'mqtt', 'embedded', 'product']},
         {'weight': 15, 'keywords': ['senior', 'lead', 'architecture', 'technical lead', 'staff', 'principal', 'design', 'mentor']},
         {'weight': 10, 'keywords': ['3d printing', 'manufacturing', 'cad', 'design', 'engineering', 'hardware', 'print']},
         {'weight': 15, 'keywords': ['pune', 'maharashtra', 'india', 'south india', 'mumbai', 'hyderabad', 'bangalore']}
     ]},
    {'id': 14, 'col': '14_Vinyl_Smart_Contract', 'title': 'Smart Contract Developer', 'company': 'Vinyl Equity', 'location': 'Mangaluru',
     'pillars': [
         {'weight': 25, 'keywords': ['solidity', 'smart contract', 'ethereum', 'evm', 'web3', 'hardhat', 'foundry', 'truffle', 'contract']},
         {'weight': 20, 'keywords': ['blockchain', 'multi-chain', 'polygon', 'solana', 'avalanche', 'layer 2', 'l2', 'cross-chain', 'bridge']},
         {'weight': 15, 'keywords': ['security', 'audit', 'vulnerability', 'reentrancy', 'overflow', 'formal verification', 'slither', 'mythril']},
         {'weight': 15, 'keywords': ['defi', 'dapp', 'token', 'dao', 'amm', 'lending', 'testing', 'unit test', 'integration test']},
         {'weight': 10, 'keywords': ['poc', 'prototype', 'greenfield', 'mvp', 'proof of concept', 'milestone', 'agile']},
         {'weight': 15, 'keywords': ['mangaluru', 'mangalore', 'nitk', 'manipal', 'udupi', 'karnataka', 'kerala', 'south india', 'bangalore', 'bengaluru']}
     ]},
]

LOCATION_SCORES = {
    'mangaluru': 20, 'mangalore': 20, 'nitk': 20, 'manipal': 20, 'udupi': 20,
    'karnataka': 18, 'kerala': 16, 'bangalore': 15, 'bengaluru': 15,
    'south india': 14, 'chennai': 12, 'hyderabad': 10, 'pune': 8,
    'india': 10, 'mumbai': 8,
    'bay area': 15, 'san francisco': 15, 'sf': 15, 'palo alto': 15,
    'california': 13, 'los angeles': 10, 'seattle': 10,
    'chicago': 15, 'illinois': 14, 'midwest': 12,
    'united states': 8, 'us': 8, 'usa': 8, 'new york': 8, 'austin': 8,
    'remote': 10, 'anywhere': 8,
}


def is_empty(val):
    if pd.isna(val):
        return True
    s = str(val).strip()
    return s == '' or s.lower() in ['nan', 'none', 'n/a', 'na', 'null']


def clean_link(l):
    if pd.isna(l):
        return None
    l = str(l).strip().lower()
    if l in ['nan', 'none', '']:
        return None
    return l


def make_composite_key(name, email, contact):
    c_name = str(name).lower().strip()
    c_email = str(email).lower().strip() if not is_empty(email) else ''
    c_contact = str(contact).lower().strip() if not is_empty(contact) else ''
    c_contact = re.sub(r'[^0-9]', '', c_contact)
    return f"{c_name}||{c_email}||{c_contact}"


def parse_experience_to_years(exp_str):
    if not exp_str:
        return 0.0
    s = str(exp_str).strip().lower()
    
    # Common zero representations
    if s in ['nan', 'none', '', 'fresher', 'no experience', 'n/a', '0', '0.0', '0 yrs', '0 years']:
        return 0.0
        
    # Check for year and month patterns
    year_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:yr|year)', s)
    month_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:month|mth)', s)
    
    years = 0.0
    months = 0.0
    
    if year_match:
        years = float(year_match.group(1))
    if month_match:
        months = float(month_match.group(1))
        
    if year_match or month_match:
        total = years + (months / 12.0)
        return round(total, 1)
        
    # Float/int fallback
    num_match = re.search(r'(\d+(?:\.\d+)?)', s)
    if num_match:
        total = float(num_match.group(1))
        return round(total, 1)
        
    return 0.0


def clean_experience(exp):
    val = parse_experience_to_years(exp)
    return f"{val:.1f} yrs"


def get_experience_years(exp_str):
    return parse_experience_to_years(exp_str)


def score_pillar_long(candidate, pillar):
    text = candidate['all_text']
    keywords = pillar['keywords']
    weight = pillar['weight']

    matches = 0.0
    for kw in keywords:
        if kw in text:
            matches += 1.0
            if kw in candidate.get('usp', '').lower():
                matches += 0.5

    max_possible = len(keywords)
    if max_possible == 0:
        return 0.0

    density = matches / max_possible

    if density >= 0.5:
        score = weight * 0.9
    elif density >= 0.3:
        score = weight * 0.7
    elif density >= 0.15:
        score = weight * 0.5
    elif density >= 0.05:
        score = weight * 0.3
    else:
        score = weight * 0.1

    return round(score, 1)


def score_pillar_short(candidate, pillar):
    text = candidate['all_text']
    keywords = pillar['keywords']
    weight = pillar['weight']

    matches = 0.0
    for kw in keywords:
        if kw in text:
            matches += 1.0
            if kw in candidate.get('usp', '').lower():
                matches += 0.5

    # Short description keyword fit (unbiased)
    if matches >= 2.0:
        score = weight * 0.9
    elif matches >= 1.0:
        score = weight * 0.6
    else:
        score = weight * 0.1

    return round(score, 1)


def score_location(candidate, role):
    text = candidate['all_text']
    pillar = role['pillars'][5]
    weight = pillar['weight']

    best = 0
    for loc, score in LOCATION_SCORES.items():
        if loc in text:
            best = max(best, score)

    college = candidate.get('college', '').lower()
    for loc, score in LOCATION_SCORES.items():
        if loc in college:
            best = max(best, int(score * 0.8))

    normalized = min(best / 20.0, 1.0)
    return round(weight * normalized, 1)


def evaluate_candidate(candidate, role, has_resume=True):
    pillar_scores = []
    for i, pillar in enumerate(role['pillars']):
        if i == 5:
            score = score_location(candidate, role)
        else:
            if has_resume:
                score = score_pillar_long(candidate, pillar)
            else:
                score = score_pillar_short(candidate, pillar)
        pillar_scores.append(score)

    base_score = sum(pillar_scores)

    exp = candidate.get('exp_years', 0.0)
    seniority = role.get('title', '').lower()
    if 'senior' in seniority or 'lead' in seniority:
        if exp >= 7: adj = 2
        elif exp >= 4: adj = 1
        elif exp >= 2: adj = 0
        else: adj = -1
    elif 'founding' in seniority:
        if exp >= 5: adj = 1.5
        elif exp >= 3: adj = 0.5
        else: adj = 0
    else:
        if exp >= 3: adj = 1
        elif exp >= 1: adj = 0
        else: adj = -0.5

    final_score = base_score + adj
    
    # Apply lower confidence penalty if candidate has no resume
    if not has_resume:
        final_score *= 0.6

    final_score = max(0.0, min(100.0, final_score))
    return round(final_score, 1)


def parse_resumes():
    with open(RESUMES_FILE) as f:
        content = f.read()

    candidates = []
    entries = content.split('# Resume #')[1:]

    for e in entries:
        lines = e.strip().split('\n')
        idx_match = re.match(r'(\d+):', lines[0])
        if not idx_match:
            continue
        idx = int(idx_match.group(1)) - 1

        c = {'idx': idx}
        for line in lines:
            m = re.match(r'\|\s*\*\*(.+?)\*\*\s*\|\s*(.+?)\s*\|', line)
            if m:
                key, val = m.group(1), m.group(2).strip()
                if key == 'Name': c['name'] = val
                elif key == 'Email 1': c['email'] = val
                elif key == 'Contact': c['contact'] = val
                elif key == 'Organisation': c['org'] = val
                elif key == 'College': c['college'] = val
                elif key == 'Experience': c['experience'] = val
                elif key == 'USP': c['usp'] = val
                elif key == 'Resume Link': c['link'] = val
                elif key == 'Drive Link': c['link'] = val

        if c.get('name'):
            content_start = e.find('## Resume Content')
            if content_start >= 0:
                c['resume_text'] = e[content_start + len('## Resume Content'):].strip()
            else:
                c['resume_text'] = ''

            c['has_resume'] = 'Yes'
            c['confidence'] = 1.0
            candidates.append(c)

    return candidates


def main():
    print("Loading datasets...")
    # Load resumes from md
    res_candidates = parse_resumes()
    print(f"  Parsed {len(res_candidates)} candidate resumes from markdown.")

    # Load Amex form responses CSV
    df_amex = pd.read_csv(AMEX_FILE)
    df_amex['Name'] = (df_amex['First Name'].fillna('') + ' ' + df_amex['Last Name'].fillna('')).str.strip()
    df_amex['clean_name'] = df_amex['Name'].str.lower().str.strip()
    df_amex['clean_link'] = df_amex['Resume'].apply(clean_link)

    # Email extraction helper
    def get_amex_email(row):
        email = row['Email Address']
        if is_empty(email): email = row['Email Id']
        if is_empty(email): email = row['Email Id ( Mandatory )']
        return str(email).lower().strip() if not is_empty(email) else ''

    # Contact extraction helper
    def get_amex_contact(row):
        contact = row['Contact No.']
        if is_empty(contact): return ''
        return re.sub(r'[^0-9]', '', str(contact).strip())

    df_amex['clean_email'] = df_amex.apply(get_amex_email, axis=1)
    df_amex['clean_contact'] = df_amex.apply(get_amex_contact, axis=1)
    df_amex['composite_key'] = df_amex.apply(
        lambda r: make_composite_key(r['Name'], r['clean_email'], r['clean_contact']), axis=1
    )

    # 1. Build maps of Amex entries for enrichment
    amex_by_link_agg = {}
    for link, group in df_amex.groupby('clean_link'):
        orgs = [o for o in group['Current Organisation'].dropna().tolist() if not is_empty(o)]
        exps = [e for e in group['Total Years of Work Experience'].dropna().tolist() if not is_empty(e)]
        colls = [c for c in group['College / University Name'].dropna().tolist() if not is_empty(c)]
        emails = []
        for col in ['Email Address', 'Email Id', 'Email Id ( Mandatory )']:
            emails.extend(group[col].dropna().tolist())
        emails = [e for e in emails if not is_empty(e)]
        contacts = [c for c in group['Contact No.'].dropna().tolist() if not is_empty(c)]
        res_links = [r for r in group['Resume'].dropna().tolist() if not is_empty(r)]
        usps = []
        for col in ['What is your Unique Selling Point', 'Unique Selling Point about you - Why should you be hired in 100 Words ?']:
            usps.extend(group[col].dropna().tolist())
        usps = [u for u in usps if not is_empty(u)]
        
        amex_by_link_agg[link] = {
            'org': orgs[0] if orgs else None,
            'exp': exps[0] if exps else None,
            'coll': colls[0] if colls else None,
            'email': emails[0] if emails else None,
            'contact': contacts[0] if contacts else None,
            'resume_link': res_links[0] if res_links else None,
            'usp': usps[0] if usps else None
        }

    amex_by_composite_agg = {}
    for key, group in df_amex.groupby('composite_key'):
        orgs = [o for o in group['Current Organisation'].dropna().tolist() if not is_empty(o)]
        exps = [e for e in group['Total Years of Work Experience'].dropna().tolist() if not is_empty(e)]
        colls = [c for c in group['College / University Name'].dropna().tolist() if not is_empty(c)]
        emails = []
        for col in ['Email Address', 'Email Id', 'Email Id ( Mandatory )']:
            emails.extend(group[col].dropna().tolist())
        emails = [e for e in emails if not is_empty(e)]
        contacts = [c for c in group['Contact No.'].dropna().tolist() if not is_empty(c)]
        res_links = [r for r in group['Resume'].dropna().tolist() if not is_empty(r)]
        usps = []
        for col in ['What is your Unique Selling Point', 'Unique Selling Point about you - Why should you be hired in 100 Words ?']:
            usps.extend(group[col].dropna().tolist())
        usps = [u for u in usps if not is_empty(u)]
        
        amex_by_composite_agg[key] = {
            'org': orgs[0] if orgs else None,
            'exp': exps[0] if exps else None,
            'coll': colls[0] if colls else None,
            'email': emails[0] if emails else None,
            'contact': contacts[0] if contacts else None,
            'resume_link': res_links[0] if res_links else None,
            'usp': usps[0] if usps else None
        }

    amex_by_name_agg = {}
    for name_lower, group in df_amex.groupby('clean_name'):
        orgs = [o for o in group['Current Organisation'].dropna().tolist() if not is_empty(o)]
        exps = [e for e in group['Total Years of Work Experience'].dropna().tolist() if not is_empty(e)]
        colls = [c for c in group['College / University Name'].dropna().tolist() if not is_empty(c)]
        emails = []
        for col in ['Email Address', 'Email Id', 'Email Id ( Mandatory )']:
            emails.extend(group[col].dropna().tolist())
        emails = [e for e in emails if not is_empty(e)]
        contacts = [c for c in group['Contact No.'].dropna().tolist() if not is_empty(c)]
        res_links = [r for r in group['Resume'].dropna().tolist() if not is_empty(r)]
        usps = []
        for col in ['What is your Unique Selling Point', 'Unique Selling Point about you - Why should you be hired in 100 Words ?']:
            usps.extend(group[col].dropna().tolist())
        usps = [u for u in usps if not is_empty(u)]
        
        amex_by_name_agg[name_lower] = {
            'org': orgs[0] if orgs else None,
            'exp': exps[0] if exps else None,
            'coll': colls[0] if colls else None,
            'email': emails[0] if emails else None,
            'contact': contacts[0] if contacts else None,
            'resume_link': res_links[0] if res_links else None,
            'usp': usps[0] if usps else None
        }

    # 2. Enrich represented candidates (the ones who have resumes)
    represented_composite_keys = set()
    represented_links = set()
    
    final_candidates = []
    
    for c in res_candidates:
        name_key = c['clean_name'] = c['name'].lower().strip()
        link_key = c['clean_link'] = clean_link(c.get('link'))
        
        email_key = c.get('email', '')
        contact_key = c.get('contact', '')
        composite_key = make_composite_key(c['name'], email_key, contact_key)
        
        represented_composite_keys.add(composite_key)
        if link_key:
            represented_links.add(link_key)
            
        # Enrich from Amex maps
        match_data = amex_by_link_agg.get(link_key)
        if not match_data:
            match_data = amex_by_composite_agg.get(composite_key)
        if not match_data:
            match_data = amex_by_name_agg.get(name_key)
            
        # Clean details
        email = c.get('email')
        if is_empty(email) and match_data: email = match_data['email']
        if is_empty(email): email = "Not Provided"
        
        contact = c.get('contact')
        if is_empty(contact) and match_data: contact = match_data['contact']
        if is_empty(contact): contact = "Not Provided"
        
        org = c.get('org')
        if is_empty(org) and match_data: org = match_data['org']
        if is_empty(org): org = "Fresher"
        
        coll = c.get('college')
        if is_empty(coll) and match_data: coll = match_data['coll']
        if is_empty(coll): coll = "Not Provided"
        
        exp = c.get('experience')
        if is_empty(exp) and match_data: exp = match_data['exp']
        exp = clean_experience(exp)
        
        r_link = c.get('link')
        if is_empty(r_link) and match_data: r_link = match_data['resume_link']
        if is_empty(r_link): r_link = "Not Provided"
        
        usp = c.get('usp')
        if is_empty(usp) and match_data: usp = match_data['usp']
        if is_empty(usp): usp = ""
        
        c['name'] = c['name']
        c['email'] = email
        c['contact'] = contact
        c['org'] = org
        c['college'] = coll
        c['experience'] = exp
        c['link'] = r_link
        c['usp'] = usp
        c['exp_years'] = get_experience_years(exp)
        
        c['all_text'] = ' '.join([
            c['name'], c['org'], c['college'], c['usp'], c.get('resume_text', '')
        ]).lower()
        
        final_candidates.append(c)

    print(f"  Enriched {len(final_candidates)} represented candidates with resume details.")

    # 3. Identify and parse unrepresented candidates (the ones without resumes)
    represented_indices = set()
    for idx, row in df_amex.iterrows():
        link = row['clean_link']
        key = row['composite_key']
        if link and link in represented_links:
            represented_indices.add(idx)
        elif key in represented_composite_keys:
            represented_indices.add(idx)

    unrepresented_df = df_amex.loc[~df_amex.index.isin(represented_indices)].copy()
    print(f"  Found {len(unrepresented_df)} unrepresented profile submission rows in Amex CSV.")

    # Deduplicate unrepresented by composite_key, keeping the best record
    def get_sort_score(row):
        usp_col1 = str(row['What is your Unique Selling Point']).strip()
        usp_col2 = str(row['Unique Selling Point about you - Why should you be hired in 100 Words ?']).strip()
        usp = usp_col1 if not is_empty(usp_col1) else usp_col2
        usp_len = len(usp) if not is_empty(usp) else 0
        has_org = 1 if not pd.isna(row['Current Organisation']) else 0
        has_coll = 1 if not pd.isna(row['College / University Name']) else 0
        return (usp_len, has_org, has_coll)

    unrepresented_df['sort_score'] = unrepresented_df.apply(get_sort_score, axis=1)
    unrepresented_sorted = unrepresented_df.sort_values(by='sort_score', ascending=False)
    unrepresented_deduped = unrepresented_sorted.drop_duplicates(subset=['composite_key'], keep='first')
    
    print(f"  Deduplicated unrepresented profiles count: {len(unrepresented_deduped)}")

    # Add unrepresented candidates to evaluation
    for idx, row in unrepresented_deduped.iterrows():
        name = row['Name']
        
        # Combine email columns
        email = row['clean_email']
        if is_empty(email): email = "Not Provided"
        
        contact = row['Contact No.']
        if is_empty(contact): contact = "Not Provided"
        
        org = row['Current Organisation']
        if is_empty(org): org = "Fresher"
        
        coll = row['College / University Name']
        if is_empty(coll): coll = "Not Provided"
        
        exp = row['Total Years of Work Experience']
        exp = clean_experience(exp)
        
        r_link = row['Resume']
        if is_empty(r_link): r_link = "Not Provided"
        
        usp_col1 = str(row['What is your Unique Selling Point']).strip()
        usp_col2 = str(row['Unique Selling Point about you - Why should you be hired in 100 Words ?']).strip()
        
        # Combine both descriptions if available
        if not is_empty(usp_col1) and not is_empty(usp_col2) and usp_col1 != usp_col2:
            usp = usp_col1 + " " + usp_col2
        elif not is_empty(usp_col1):
            usp = usp_col1
        elif not is_empty(usp_col2):
            usp = usp_col2
        else:
            usp = ""
            
        c = {
            'name': name,
            'email': email,
            'contact': contact,
            'org': org,
            'college': coll,
            'experience': exp,
            'link': r_link,
            'usp': usp,
            'has_resume': 'No',
            'confidence': 0.6,
            'exp_years': get_experience_years(exp),
            'resume_text': ''
        }
        
        c['all_text'] = ' '.join([
            c['name'], c['org'], c['college'], c['usp']
        ]).lower()
        
        final_candidates.append(c)

    print(f"Total candidates to evaluate: {len(final_candidates)}")

    # 4. Score all candidates against 14 roles
    print("Scoring candidates against 14 job roles...")
    rows = []
    
    for c in final_candidates:
        row = {
            'Name': c['name'],
            'Email': c['email'],
            'Contact': c['contact'],
            'Organisation': c['org'],
            'College': c['college'],
            'Experience': c['experience'],
            'Resume Link': c['link'],
            'Has Resume': c['has_resume'],
            'Confidence': c['confidence']
        }
        
        has_res = (c['has_resume'] == 'Yes')
        
        for role in ROLES:
            score = evaluate_candidate(c, role, has_resume=has_res)
            row[role['col']] = score
            
        row['Total'] = round(sum(row[r['col']] for r in ROLES), 1)
        rows.append(row)

    # Sort descending by Total score
    rows.sort(key=lambda x: x['Total'], reverse=True)

    # 5. Write to evaluation_results.csv
    fieldnames = ['Name', 'Email', 'Contact', 'Organisation', 'College', 'Experience', 'Resume Link', 'Has Resume', 'Confidence']
    fieldnames += [r['col'] for r in ROLES]
    fieldnames.append('Total')

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    
    with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nDone! Written {len(rows)} candidates to: {OUTPUT_FILE}")

    # 6. Report metrics and top profiles
    print("\n--- COLUMN FILL RATE COMPARISON (Final Enriched Dataset) ---")
    total_rows = len(rows)
    cols_to_check = ['Name', 'Email', 'Contact', 'Organisation', 'College', 'Experience', 'Resume Link', 'Has Resume', 'Confidence']
    
    for col in cols_to_check:
        null_count = sum(1 for r in rows if r[col] is None or str(r[col]).strip() == '' or str(r[col]).lower() == 'nan')
        fill_count = total_rows - null_count
        fill_pct = (fill_count / total_rows) * 100
        print(f"Column: {col} | Non-Null: {fill_count}/{total_rows} ({fill_pct:.2f}%)")
        
    print("\nTop 10 candidates by total score:")
    for i, r in enumerate(rows[:10]):
        scores = [f"{role['col']}={r[role['col']]}" for role in ROLES if r[role['col']] >= 15]
        print(f"  {i+1}. {r['Name']:25s} | Has Resume: {r['Has Resume']} | Total: {r['Total']:5.1f} | Org: {r['Organisation'][:20]} | Top: {', '.join(scores[:3])}")


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
Security Audit Script for BotSmith
Checks for exposed secrets, vulnerable configurations, and security issues
"""
import os
import re
import json
from pathlib import Path
from typing import List, Dict

# Patterns for sensitive data
SENSITIVE_PATTERNS = {
    'OpenAI API Key': r'sk-[a-zA-Z0-9]{20,}',
    'Anthropic API Key': r'sk-ant-[a-zA-Z0-9-]{20,}',
    'Google API Key': r'AIza[a-zA-Z0-9_-]{35}',
    'AWS Access Key': r'AKIA[a-zA-Z0-9]{16}',
    'GitHub Token': r'gh[pousr]_[a-zA-Z0-9]{36}',
    'Private Key': r'-----BEGIN (RSA|DSA|EC|OPENSSH) PRIVATE KEY-----',
    'Generic API Key': r'api[_-]?key["\']?\s*[:=]\s*["\'][a-zA-Z0-9]{20,}["\']',
    'Secret Key': r'secret[_-]?key["\']?\s*[:=]\s*["\'][a-zA-Z0-9]{20,}["\']',
    'Password': r'password["\']?\s*[:=]\s*["\'][^"\']{8,}["\']',
    'MongoDB URI': r'mongodb(\+srv)?://[^\s]+',
    'Database URL': r'(postgres|mysql|redis)://[^\s]+',
    'JWT Secret': r'jwt[_-]?secret["\']?\s*[:=]\s*["\'][a-zA-Z0-9]{20,}["\']',
}

# Files to ignore
IGNORE_PATTERNS = [
    'node_modules',
    '.git',
    '__pycache__',
    '*.pyc',
    'venv',
    '.venv',
    'build',
    'dist',
    '*.min.js',
    'package-lock.json',
    'yarn.lock',
]

# Safe environment variable names (should be in .env, not code)
SAFE_ENV_VARS = [
    'REACT_APP_BACKEND_URL',
    'NODE_ENV',
    'PORT',
    'HOST',
]

def should_ignore(filepath: Path) -> bool:
    """Check if file should be ignored"""
    path_str = str(filepath)
    for pattern in IGNORE_PATTERNS:
        if pattern in path_str:
            return True
    return False

def scan_file(filepath: Path) -> List[Dict]:
    """Scan a single file for sensitive data"""
    findings = []
    
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
        for name, pattern in SENSITIVE_PATTERNS.items():
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                # Get line number
                line_num = content[:match.start()].count('\n') + 1
                
                findings.append({
                    'type': name,
                    'file': str(filepath),
                    'line': line_num,
                    'match': match.group()[:50] + '...' if len(match.group()) > 50 else match.group(),
                })
    except Exception as e:
        pass
    
    return findings

def scan_directory(directory: Path) -> List[Dict]:
    """Recursively scan directory for sensitive data"""
    all_findings = []
    
    for filepath in directory.rglob('*'):
        if filepath.is_file() and not should_ignore(filepath):
            # Only scan text files
            if filepath.suffix in ['.py', '.js', '.jsx', '.ts', '.tsx', '.json', '.yaml', '.yml', '.env', '.txt', '.md', '.sh']:
                findings = scan_file(filepath)
                all_findings.extend(findings)
    
    return all_findings

def check_environment_files():
    """Check .env files for security issues"""
    issues = []
    
    env_files = [
        '/app/backend/.env',
        '/app/frontend/.env',
        '/app/.env',
    ]
    
    for env_file in env_files:
        if os.path.exists(env_file):
            print(f"✓ Found environment file: {env_file}")
            
            # Check if file is in .gitignore
            gitignore_path = os.path.join(os.path.dirname(env_file), '.gitignore')
            if os.path.exists(gitignore_path):
                with open(gitignore_path, 'r') as f:
                    gitignore_content = f.read()
                    if '.env' not in gitignore_content:
                        issues.append({
                            'severity': 'HIGH',
                            'issue': f'.env file not in .gitignore at {os.path.dirname(env_file)}',
                            'recommendation': 'Add .env to .gitignore'
                        })
    
    return issues

def check_cors_configuration():
    """Check CORS configuration"""
    issues = []
    
    server_file = '/app/backend/server.py'
    if os.path.exists(server_file):
        with open(server_file, 'r') as f:
            content = f.read()
            
        # Check for wildcard CORS
        if "allow_origins=['*']" in content or 'allow_origins=["*"]' in content:
            issues.append({
                'severity': 'MEDIUM',
                'issue': 'CORS allows all origins (*)',
                'recommendation': 'Restrict CORS to specific domains in production'
            })
    
    return issues

def check_security_headers():
    """Check if security headers are implemented"""
    issues = []
    
    server_file = '/app/backend/server.py'
    if os.path.exists(server_file):
        with open(server_file, 'r') as f:
            content = f.read()
            
        required_headers = [
            ('X-Content-Type-Options', 'nosniff header'),
            ('X-Frame-Options', 'clickjacking protection'),
            ('Strict-Transport-Security', 'HSTS'),
        ]
        
        for header, description in required_headers:
            if header not in content:
                issues.append({
                    'severity': 'MEDIUM',
                    'issue': f'Missing security header: {header}',
                    'recommendation': f'Implement {description}'
                })
    
    return issues

def generate_report(findings: List[Dict], env_issues: List[Dict], 
                   cors_issues: List[Dict], header_issues: List[Dict]):
    """Generate security audit report"""
    
    print("\n" + "="*80)
    print("🔒 SECURITY AUDIT REPORT - BotSmith")
    print("="*80 + "\n")
    
    # Exposed Secrets
    if findings:
        print(f"⚠️  CRITICAL: Found {len(findings)} potential exposed secrets:\n")
        for finding in findings[:10]:  # Show first 10
            print(f"  Type: {finding['type']}")
            print(f"  File: {finding['file']}")
            print(f"  Line: {finding['line']}")
            print(f"  Match: {finding['match']}")
            print()
        
        if len(findings) > 10:
            print(f"  ... and {len(findings) - 10} more\n")
    else:
        print("✅ No exposed secrets found in code\n")
    
    # Environment Issues
    if env_issues:
        print(f"⚠️  Found {len(env_issues)} environment configuration issues:\n")
        for issue in env_issues:
            print(f"  [{issue['severity']}] {issue['issue']}")
            print(f"  → {issue['recommendation']}\n")
    else:
        print("✅ Environment configuration looks good\n")
    
    # CORS Issues
    if cors_issues:
        print(f"⚠️  Found {len(cors_issues)} CORS configuration issues:\n")
        for issue in cors_issues:
            print(f"  [{issue['severity']}] {issue['issue']}")
            print(f"  → {issue['recommendation']}\n")
    else:
        print("✅ CORS configuration is secure\n")
    
    # Security Headers
    if header_issues:
        print(f"⚠️  Found {len(header_issues)} security header issues:\n")
        for issue in header_issues:
            print(f"  [{issue['severity']}] {issue['issue']}")
            print(f"  → {issue['recommendation']}\n")
    else:
        print("✅ Security headers are implemented\n")
    
    # Overall Score
    total_issues = len(findings) + len(env_issues) + len(cors_issues) + len(header_issues)
    
    if total_issues == 0:
        print("="*80)
        print("🎉 EXCELLENT: No security issues found!")
        print("="*80 + "\n")
        return 0
    else:
        print("="*80)
        print(f"⚠️  TOTAL ISSUES FOUND: {total_issues}")
        print("="*80 + "\n")
        return total_issues

if __name__ == '__main__':
    print("Starting security audit...\n")
    
    # Scan frontend
    print("Scanning frontend code...")
    frontend_findings = scan_directory(Path('/app/frontend/src'))
    
    # Scan backend
    print("Scanning backend code...")
    backend_findings = scan_directory(Path('/app/backend'))
    
    all_findings = frontend_findings + backend_findings
    
    # Check environment files
    print("Checking environment configuration...")
    env_issues = check_environment_files()
    
    # Check CORS
    print("Checking CORS configuration...")
    cors_issues = check_cors_configuration()
    
    # Check security headers
    print("Checking security headers...")
    header_issues = check_security_headers()
    
    # Generate report
    exit_code = generate_report(all_findings, env_issues, cors_issues, header_issues)
    
    exit(exit_code)

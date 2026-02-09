"""
Agent 2 Standalone Test
Test resume customization without Google Sheets
"""

import os
from agent_2_resume_customizer import ResumeCustomizer

def test_agent_2():
    """Test Agent 2 with a sample job"""
    
    print("🧪 Testing Agent 2: Resume Customizer\n")
    print("="*60)
    
    # Sample job for testing
    sample_job = {
        'Job ID': 'TEST001',
        'Title': 'Senior Product Manager - AI/ML',
        'Company': 'TechCorp India',
        'Link': '',  # No real link for test
        'Status': 'New'
    }
    
    # Sample job description
    sample_description = """
We are seeking a Senior Product Manager to lead our AI/ML products team. 

Responsibilities:
- Define product roadmap for AI-powered features
- Work with data scientists and ML engineers
- Conduct A/B testing and analyze user data using SQL
- Manage stakeholder relationships across engineering, design, and business
- Lead agile product development process

Requirements:
- 5+ years of product management experience
- Strong technical background with SQL and Python
- Experience with AI/ML products
- Proven track record of launching data-driven features
- Excellent stakeholder management skills
- Experience with B2B SaaS or consumer tech

Nice to have:
- MBA or technical degree
- Experience in Indian tech ecosystem
- Knowledge of recommendation systems
    """
    
    print("\n📋 Test Job:")
    print(f"   Title: {sample_job['Title']}")
    print(f"   Company: {sample_job['Company']}")
    print(f"   Description: {len(sample_description)} characters")
    
    # Initialize Agent 2 (without Google Sheets)
    customizer = ResumeCustomizer(
        master_resume_path="resume_master.docx",
        use_sheets=False
    )
    
    # Test AI analysis
    print("\n" + "="*60)
    print("Testing AI Analysis...")
    print("="*60)
    
    analysis = customizer.analyze_job_with_ai(
        job_title=sample_job['Title'],
        company=sample_job['Company'],
        job_description=sample_description
    )
    
    print("\n📊 Analysis Results:")
    print(f"   Required Skills: {analysis.get('required_skills', [])}")
    print(f"   Keywords: {analysis.get('keywords', [])}")
    print(f"   Seniority: {analysis.get('seniority', 'Unknown')}")
    print(f"   Domain: {analysis.get('domain', 'Unknown')}")
    
    # Test match scoring
    print("\n" + "="*60)
    print("Testing Match Scoring...")
    print("="*60)
    
    try:
        from docx import Document
        master_doc = Document("resume_master.docx")
        master_text = '\n'.join([p.text for p in master_doc.paragraphs])
        
        match_score = customizer.calculate_match_score(analysis, master_text)
        print(f"\n   📈 Match Score: {match_score}%")
        
        if match_score >= customizer.config['auto_approve_score']:
            print(f"   ✅ Strong match - auto-approve for Agent 3")
        elif match_score >= customizer.config['min_match_score']:
            print(f"   ⚠️  Moderate match - needs review")
        else:
            print(f"   ❌ Low match - would skip")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test resume customization
    print("\n" + "="*60)
    print("Testing Resume Customization...")
    print("="*60)
    
    test_folder = "test_output"
    os.makedirs(test_folder, exist_ok=True)
    
    resume_path = os.path.join(test_folder, "Test_Resume.docx")
    cover_letter_path = os.path.join(test_folder, "Test_CoverLetter.docx")
    
    resume_success = customizer.customize_resume(
        job_title=sample_job['Title'],
        company=sample_job['Company'],
        analysis=analysis,
        output_path=resume_path
    )
    
    cover_success = customizer.generate_cover_letter(
        job_title=sample_job['Title'],
        company=sample_job['Company'],
        analysis=analysis,
        output_path=cover_letter_path
    )
    
    print("\n" + "="*60)
    print("✅ Test Complete!")
    print("="*60)
    
    if resume_success:
        print(f"\n📄 Resume: {resume_path}")
    if cover_success:
        print(f"📄 Cover Letter: {cover_letter_path}")
    
    print(f"\n💡 Check the '{test_folder}' folder to review the generated documents")
    
    # Summary
    print("\n" + "="*60)
    print("Test Results Summary:")
    print("="*60)
    print(f"   AI Analysis: {'✅ Working' if analysis else '❌ Failed'}")
    print(f"   Match Scoring: {'✅ Working' if match_score else '❌ Failed'}")
    print(f"   Resume Creation: {'✅ Working' if resume_success else '❌ Failed'}")
    print(f"   Cover Letter: {'✅ Working' if cover_success else '❌ Failed'}")
    
    if analysis and match_score and resume_success:
        print("\n🎉 Agent 2 is working! Ready to process real jobs.")
    else:
        print("\n⚠️  Some tests failed. Check errors above.")


if __name__ == "__main__":
    # Check requirements
    if not os.path.exists("resume_master.docx"):
        print("❌ resume_master.docx not found!")
        print("💡 Run: node create_mock_resume.js")
        exit(1)
    
    if not os.environ.get('OPENAI_API_KEY'):
        print("⚠️  OPENAI_API_KEY not set")
        print("   Some features will be limited")
        print("   To get full functionality:")
        print("   export OPENAI_API_KEY='your-key-here'\n")
    
    test_agent_2()

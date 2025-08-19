"""
JARVIS AI Agent - Enhanced Research Service
Handles automated online research with interactive workflows and report generation
"""
import asyncio
import time
import json
import markdown
from typing import Dict, Any, List, Tuple, Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import subprocess
import tempfile
import os
import uuid
from datetime import datetime
from pathlib import Path

class ResearchWorkflow:
    """Represents an interactive research workflow"""
    
    def __init__(self, topic: str, session_id: str):
        self.topic = topic
        self.session_id = session_id
        self.phase = "initial"  # initial, proposal, user_choice, execution, report, complete
        self.proposals = []
        self.selected_proposal = None
        self.research_data = []
        self.report = None
        self.created_at = datetime.now()
        
class ResearchProposal:
    """Represents a research approach proposal"""
    
    def __init__(self, title: str, description: str, sources: List[str], 
                 complexity: str, estimated_time: int, pros: List[str], cons: List[str]):
        self.title = title
        self.description = description
        self.sources = sources
        self.complexity = complexity  # "simple", "moderate", "comprehensive"
        self.estimated_time = estimated_time  # minutes
        self.pros = pros
        self.cons = cons
        self.confidence_score = 0.0

class ResearchService:
    """Enhanced service for automated online research with interactive workflows"""
    
    def __init__(self):
        self.research_sessions = {}  # Track active research sessions
        self.active_workflows = {}   # Track interactive workflows
        self.temp_data_dir = tempfile.mkdtemp(prefix="jarvis_research_")
        self.reports_dir = Path("jarvis_reports")
        self.reports_dir.mkdir(exist_ok=True)
        
    async def start_interactive_research(self, topic: str, user_preferences: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Start an interactive research workflow
        Phase 1: Generate research proposals
        """
        workflow_id = str(uuid.uuid4())[:8]
        workflow = ResearchWorkflow(topic, workflow_id)
        
        try:
            # Generate research proposals
            proposals = await self._generate_research_proposals(topic, user_preferences)
            workflow.proposals = proposals
            workflow.phase = "proposal"
            
            self.active_workflows[workflow_id] = workflow
            
            return {
                "workflow_id": workflow_id,
                "phase": "proposal",
                "topic": topic,
                "proposals": [
                    {
                        "title": p.title,
                        "description": p.description,
                        "sources": p.sources,
                        "complexity": p.complexity,
                        "estimated_time": p.estimated_time,
                        "pros": p.pros,
                        "cons": p.cons,
                        "confidence_score": p.confidence_score
                    } for p in proposals
                ],
                "message": f"I've analyzed '{topic}' and generated {len(proposals)} research approaches. Please review and select your preferred option, or let me choose the best one.",
                "next_action": "Please respond with: 'option 1', 'option 2', 'option 3', or 'choose for me'"
            }
            
        except Exception as e:
            return {"error": f"Failed to start research workflow: {str(e)}"}
    
    async def _generate_research_proposals(self, topic: str, user_preferences: Dict[str, Any] = None) -> List[ResearchProposal]:
        """Generate different research approach proposals"""
        proposals = []
        
        # Proposal 1: Quick Overview
        proposals.append(ResearchProposal(
            title="Quick Overview Research",
            description=f"Rapid survey of {topic} using top search results and popular sources",
            sources=["Google Search", "Wikipedia", "Top 3 websites"],
            complexity="simple",
            estimated_time=5,
            pros=["Fast results", "Good for initial understanding", "Low resource usage"],
            cons=["Less comprehensive", "May miss niche insights"],
            confidence_score=0.8
        ))
        
        # Proposal 2: Comprehensive Analysis
        proposals.append(ResearchProposal(
            title="Comprehensive Deep-Dive",
            description=f"Thorough investigation of {topic} across multiple platforms and sources",
            sources=["Google Search", "GitHub", "YouTube", "Academic sources", "Forums"],
            complexity="comprehensive",
            estimated_time=15,
            pros=["Very thorough", "Multiple perspectives", "High-quality insights"],
            cons=["Takes longer", "More resource intensive"],
            confidence_score=0.9
        ))
        
        # Proposal 3: Targeted Practical Focus
        proposals.append(ResearchProposal(
            title="Practical Implementation Focus",
            description=f"Focus on practical, actionable information about {topic}",
            sources=["GitHub repositories", "Tutorial sites", "Stack Overflow", "Documentation"],
            complexity="moderate",
            estimated_time=10,
            pros=["Actionable results", "Code examples", "Real-world solutions"],
            cons=["Less theoretical background", "May miss broader context"],
            confidence_score=0.85
        ))
        
        return proposals
    
    async def handle_user_choice(self, workflow_id: str, choice: str) -> Dict[str, Any]:
        """
        Handle user's research approach choice
        Phase 2: Execute chosen research
        """
        if workflow_id not in self.active_workflows:
            return {"error": "Workflow not found"}
        
        workflow = self.active_workflows[workflow_id]
        
        try:
            # Parse user choice
            if "choose for me" in choice.lower() or "auto" in choice.lower():
                # Select highest confidence proposal
                selected_idx = max(range(len(workflow.proposals)), 
                                 key=lambda i: workflow.proposals[i].confidence_score)
                selected_proposal = workflow.proposals[selected_idx]
                choice_msg = f"I've selected the '{selected_proposal.title}' approach based on optimal balance of quality and efficiency."
            else:
                # Parse user selection
                import re
                option_match = re.search(r'option\s*(\d+)', choice.lower())
                if option_match:
                    selected_idx = int(option_match.group(1)) - 1
                    if 0 <= selected_idx < len(workflow.proposals):
                        selected_proposal = workflow.proposals[selected_idx]
                        choice_msg = f"Executing your chosen approach: '{selected_proposal.title}'"
                    else:
                        return {"error": "Invalid option number"}
                else:
                    return {"error": "Please specify 'option 1', 'option 2', 'option 3', or 'choose for me'"}
            
            workflow.selected_proposal = selected_proposal
            workflow.phase = "execution"
            
            # Execute the research
            execution_result = await self._execute_research_proposal(workflow)
            
            # Generate report
            report = await self._generate_research_report(workflow)
            workflow.report = report
            workflow.phase = "report"
            
            return {
                "workflow_id": workflow_id,
                "phase": "report",
                "choice_message": choice_msg,
                "execution_summary": execution_result,
                "report": report,
                "next_action": "Would you like me to save this report? Respond with 'save report' or 'just show me'"
            }
            
        except Exception as e:
            return {"error": f"Failed to execute research: {str(e)}"}
    
    async def _execute_research_proposal(self, workflow: ResearchWorkflow) -> Dict[str, Any]:
        """Execute the selected research proposal"""
        proposal = workflow.selected_proposal
        
        try:
            if proposal.complexity == "simple":
                # Quick research - fewer sources
                result = await self.conduct_research(workflow.topic, num_tabs=2)
            elif proposal.complexity == "comprehensive":
                # Deep research - more sources
                sources = ["github.com", "youtube.com"] if "github" in proposal.sources[0].lower() else None
                result = await self.conduct_research(workflow.topic, sources=sources, num_tabs=4)
            else:
                # Moderate research
                result = await self.conduct_research(workflow.topic, num_tabs=3)
            
            workflow.research_data = result.get("results", [])
            
            return {
                "status": "completed",
                "sources_found": len(workflow.research_data),
                "quality_score": self._calculate_research_quality(workflow.research_data),
                "execution_time": proposal.estimated_time
            }
            
        except Exception as e:
            return {"status": "failed", "error": str(e)}
    
    def _calculate_research_quality(self, research_data: List[Dict[str, Any]]) -> float:
        """Calculate quality score for research results"""
        if not research_data:
            return 0.0
        
        total_score = 0.0
        for item in research_data:
            score = item.get("relevance_score", 0.0)
            # Bonus for diverse sources
            if "github" in item.get("url", "").lower():
                score += 0.2
            if any(keyword in item.get("snippet", "").lower() for keyword in ["tutorial", "guide", "example"]):
                score += 0.1
            total_score += score
        
        return min(10.0, total_score / len(research_data) * 2)
    
    async def _generate_research_report(self, workflow: ResearchWorkflow) -> Dict[str, Any]:
        """Generate a comprehensive research report"""
        proposal = workflow.selected_proposal
        
        # Generate report content
        report_content = self._create_report_markdown(workflow)
        report_html = markdown.markdown(report_content, extensions=['tables', 'fenced_code'])
        
        report = {
            "title": f"Research Report: {workflow.topic}",
            "topic": workflow.topic,
            "approach": proposal.title,
            "generated_at": datetime.now().isoformat(),
            "quality_score": self._calculate_research_quality(workflow.research_data),
            "sources_count": len(workflow.research_data),
            "content_markdown": report_content,
            "content_html": report_html,
            "executive_summary": self._generate_executive_summary(workflow),
            "recommendations": self._generate_recommendations(workflow),
            "key_findings": self._extract_key_findings(workflow.research_data)
        }
        
        return report
    
    def _create_report_markdown(self, workflow: ResearchWorkflow) -> str:
        """Create markdown formatted research report"""
        proposal = workflow.selected_proposal
        
        markdown_content = f"""# Research Report: {workflow.topic}

**Generated by JARVIS AI Research System**  
**Date:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  
**Research Approach:** {proposal.title}  
**Complexity Level:** {proposal.complexity.title()}  

## Executive Summary

{self._generate_executive_summary(workflow)}

## Research Methodology

**Selected Approach:** {proposal.description}

**Sources Investigated:**
{chr(10).join(f'- {source}' for source in proposal.sources)}

**Quality Metrics:**
- Sources Found: {len(workflow.research_data)}
- Quality Score: {self._calculate_research_quality(workflow.research_data):.1f}/10
- Confidence Level: {proposal.confidence_score:.0%}

## Key Findings

{self._format_key_findings(workflow.research_data)}

## Detailed Results

"""
        
        # Add detailed results
        for i, result in enumerate(workflow.research_data[:10], 1):  # Top 10 results
            markdown_content += f"""### {i}. {result.get('title', 'Untitled')}

**Source:** [{result.get('url', 'N/A')}]({result.get('url', '#')})  
**Relevance:** {result.get('relevance_score', 0):.1f}/10

{result.get('snippet', 'No description available.')}

---

"""
        
        markdown_content += f"""## Recommendations

{self._generate_recommendations(workflow)}

## Next Steps

Based on this research, I recommend:

1. **Immediate Actions:** Review the top 3 findings for quick implementation
2. **Deep Dive:** Explore the highest-rated sources for comprehensive understanding  
3. **Practical Application:** Consider the implementation-focused results for hands-on learning

---

*Report generated by JARVIS AI Research System v2.0*
"""
        
        return markdown_content
    
    def _generate_executive_summary(self, workflow: ResearchWorkflow) -> str:
        """Generate executive summary of research"""
        topic = workflow.topic
        data_count = len(workflow.research_data)
        quality = self._calculate_research_quality(workflow.research_data)
        
        return f"""This research investigated "{topic}" using the {workflow.selected_proposal.title.lower()} methodology. 
        
The analysis examined {data_count} relevant sources and achieved a quality score of {quality:.1f}/10. The research reveals multiple approaches and solutions related to {topic}, with particular strength in practical implementation guidance and community-driven resources."""
    
    def _generate_recommendations(self, workflow: ResearchWorkflow) -> str:
        """Generate actionable recommendations"""
        recommendations = []
        
        # Analyze research data for recommendations
        github_sources = [r for r in workflow.research_data if "github" in r.get("url", "")]
        youtube_sources = [r for r in workflow.research_data if "youtube" in r.get("url", "")]
        
        if github_sources:
            recommendations.append("Explore the GitHub repositories found for code examples and implementation details")
        
        if youtube_sources:
            recommendations.append("Watch the YouTube tutorials for visual learning and step-by-step guidance")
        
        recommendations.append("Start with the highest-rated sources for quality information")
        recommendations.append("Cross-reference multiple sources to ensure comprehensive understanding")
        
        return "\n".join(f"- {rec}" for rec in recommendations)
    
    def _format_key_findings(self, research_data: List[Dict[str, Any]]) -> str:
        """Format key findings from research data"""
        if not research_data:
            return "No significant findings to report."
        
        # Get top findings
        top_findings = sorted(research_data, key=lambda x: x.get("relevance_score", 0), reverse=True)[:5]
        
        findings = []
        for finding in top_findings:
            title = finding.get("title", "Unknown")
            snippet = finding.get("snippet", "")[:150] + "..." if len(finding.get("snippet", "")) > 150 else finding.get("snippet", "")
            findings.append(f"**{title}:** {snippet}")
        
        return "\n\n".join(findings)
    
    def _extract_key_findings(self, research_data: List[Dict[str, Any]]) -> List[str]:
        """Extract key findings as list"""
        findings = []
        for item in research_data[:5]:
            title = item.get("title", "")
            if title:
                findings.append(title)
        return findings
    
    async def save_research_report(self, workflow_id: str, save_location: str = "auto") -> Dict[str, Any]:
        """
        Save research report to file
        Phase 3: Save and complete workflow
        """
        if workflow_id not in self.active_workflows:
            return {"error": "Workflow not found"}
        
        workflow = self.active_workflows[workflow_id]
        
        if not workflow.report:
            return {"error": "No report available to save"}
        
        try:
            # Determine save location
            if save_location == "auto":
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                safe_topic = "".join(c for c in workflow.topic if c.isalnum() or c in " -_").replace(" ", "_")
                filename = f"research_{safe_topic}_{timestamp}"
            else:
                filename = save_location
            
            # Save markdown version
            md_path = self.reports_dir / f"{filename}.md"
            with open(md_path, 'w', encoding='utf-8') as f:
                f.write(workflow.report["content_markdown"])
            
            # Save HTML version
            html_path = self.reports_dir / f"{filename}.html"
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(f"""<!DOCTYPE html>
<html>
<head>
    <title>{workflow.report['title']}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }}
        h1, h2, h3 {{ color: #333; }}
        .metadata {{ background: #f5f5f5; padding: 15px; border-radius: 5px; margin: 20px 0; }}
        .finding {{ margin: 15px 0; padding: 10px; border-left: 3px solid #007acc; }}
    </style>
</head>
<body>
{workflow.report["content_html"]}
</body>
</html>""")
            
            # Save JSON version for future processing
            json_path = self.reports_dir / f"{filename}.json"
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(workflow.report, f, indent=2, default=str)
            
            # Mark workflow as complete
            workflow.phase = "complete"
            
            # Cleanup session if exists
            if workflow.session_id in self.research_sessions:
                await self.close_research_session(workflow.session_id)
            
            return {
                "status": "saved",
                "files_created": {
                    "markdown": str(md_path),
                    "html": str(html_path),
                    "json": str(json_path)
                },
                "message": f"Research report saved successfully! You can find it at {md_path.parent}",
                "workflow_completed": True
            }
            
        except Exception as e:
            return {"error": f"Failed to save report: {str(e)}"}
    
    async def get_workflow_status(self, workflow_id: str) -> Dict[str, Any]:
        """Get current status of a research workflow"""
        if workflow_id not in self.active_workflows:
            return {"error": "Workflow not found"}
        
        workflow = self.active_workflows[workflow_id]
        
        return {
            "workflow_id": workflow_id,
            "topic": workflow.topic,
            "phase": workflow.phase,
            "created_at": workflow.created_at.isoformat(),
            "proposals_count": len(workflow.proposals),
            "selected_proposal": workflow.selected_proposal.title if workflow.selected_proposal else None,
            "research_data_count": len(workflow.research_data),
            "report_ready": workflow.report is not None
        }
        
    async def conduct_research(self, topic: str, sources: List[str] = None, num_tabs: int = 3) -> Dict[str, Any]:
        """
        Conduct automated research on a topic
        
        Args:
            topic: The research topic
            sources: Optional list of specific sources/websites
            num_tabs: Number of browser tabs to open for research
            
        Returns:
            Dict with research results and session info
        """
        session_id = str(uuid.uuid4())[:8]
        
        try:
            # Create research session
            research_session = {
                "id": session_id,
                "topic": topic,
                "tabs": [],
                "results": [],
                "start_time": time.time(),
                "driver": None
            }
            
            # Initialize browser with multiple tabs capability
            driver = await self._init_research_browser()
            research_session["driver"] = driver
            
            # Define search queries based on topic
            search_queries = self._generate_search_queries(topic, sources)
            
            # Open tabs and conduct searches
            for i, query in enumerate(search_queries[:num_tabs]):
                try:
                    if i == 0:
                        # Use the main tab
                        tab_handle = driver.current_window_handle
                    else:
                        # Open new tab
                        driver.execute_script("window.open('');")
                        tab_handle = driver.window_handles[-1]
                        driver.switch_to.window(tab_handle)
                    
                    # Perform search
                    result = await self._search_in_tab(driver, query, tab_handle)
                    research_session["tabs"].append({
                        "handle": tab_handle,
                        "query": query,
                        "result": result
                    })
                    
                    # Brief delay between searches
                    await asyncio.sleep(1)
                    
                except Exception as e:
                    print(f"Error in tab {i}: {e}")
                    continue
            
            # Collect and summarize results
            research_session["results"] = await self._collect_results(research_session)
            
            # Store session
            self.research_sessions[session_id] = research_session
            
            return {
                "session_id": session_id,
                "topic": topic,
                "tabs_opened": len(research_session["tabs"]),
                "results": research_session["results"],
                "status": "completed"
            }
            
        except Exception as e:
            return {
                "session_id": session_id,
                "error": str(e),
                "status": "failed"
            }
    
    async def close_research_session(self, session_id: str = None) -> str:
        """Close research session and browser tabs"""
        try:
            if session_id and session_id in self.research_sessions:
                session = self.research_sessions[session_id]
                if session["driver"]:
                    session["driver"].quit()
                del self.research_sessions[session_id]
                return f"Research session {session_id} closed"
            else:
                # Close all sessions
                closed_count = 0
                for sid, session in list(self.research_sessions.items()):
                    if session["driver"]:
                        session["driver"].quit()
                    del self.research_sessions[sid]
                    closed_count += 1
                return f"Closed {closed_count} research sessions"
                
        except Exception as e:
            return f"Error closing research session: {str(e)}"
    
    def _generate_search_queries(self, topic: str, sources: List[str] = None) -> List[str]:
        """Generate search queries for the research topic"""
        base_queries = [
            f"{topic} best practices",
            f"{topic} guide tutorial",
            f"{topic} tips strategies",
            f"how to {topic}",
            f"{topic} examples case studies"
        ]
        
        # Add source-specific queries if provided
        if sources:
            for source in sources:
                base_queries.append(f"{topic} site:{source}")
        
        return base_queries
    
    async def _init_research_browser(self) -> webdriver.Chrome:
        """Initialize Chrome browser for research with fallback options"""
        try:
            options = Options()
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-web-security")
            options.add_argument("--allow-running-insecure-content")
            options.add_argument(f"--user-data-dir={self.temp_data_dir}")
            
            # Try different Chrome/Chromium paths with fallback
            chrome_paths = [
                "/snap/bin/chromium",
                "/usr/bin/google-chrome",
                "/usr/bin/chromium-browser",
                "/usr/bin/chromium",
                "google-chrome",
                "chromium-browser",
                "chromium"
            ]
            
            last_error = None
            driver = None
            
            for chrome_path in chrome_paths:
                try:
                    print(f"🔍 Trying browser path: {chrome_path}")
                    
                    # Check if path exists for absolute paths
                    if chrome_path.startswith("/") and not os.path.exists(chrome_path):
                        continue
                    
                    # Set binary location for absolute paths
                    if chrome_path.startswith("/"):
                        options.binary_location = chrome_path
                    
                    # Try to get ChromeDriver
                    try:
                        service = Service(ChromeDriverManager().install())
                    except Exception as e:
                        print(f"⚠️ ChromeDriver manager failed: {e}")
                        # Fallback to system chromedriver
                        service = Service("/usr/bin/chromedriver") if os.path.exists("/usr/bin/chromedriver") else None
                        if not service:
                            continue
                    
                    driver = webdriver.Chrome(service=service, options=options)
                    print(f"✅ Successfully initialized browser with: {chrome_path}")
                    break
                    
                except Exception as e:
                    last_error = e
                    print(f"❌ Failed with {chrome_path}: {e}")
                    continue
            
            if not driver:
                # Final fallback - try system open commands
                print("🔄 Browser WebDriver failed, trying system commands...")
                await self._fallback_browser_open()
                raise Exception(f"Could not initialize any browser. Last error: {last_error}")
                
            return driver
            
        except Exception as e:
            raise Exception(f"Browser initialization failed: {str(e)}")
    
    async def _fallback_browser_open(self):
        """Fallback method to open browser with system commands"""
        try:
            # Try opening browser with system commands as fallback
            browsers = ["/snap/bin/chromium", "google-chrome", "firefox"]
            for browser in browsers:
                try:
                    # Open browser with search URLs
                    urls = [
                        "https://github.com/search?q=JARVIS",
                        "https://www.youtube.com/results?search_query=JARVIS+AI+project"
                    ]
                    
                    for url in urls:
                        subprocess.Popen([browser, url], 
                                       stdout=subprocess.DEVNULL, 
                                       stderr=subprocess.DEVNULL)
                        await asyncio.sleep(2)
                    
                    print(f"✅ Opened research URLs with {browser}")
                    return True
                except:
                    continue
            return False
        except:
            return False
    
    async def _search_in_tab(self, driver: webdriver.Chrome, query: str, tab_handle: str) -> Dict[str, Any]:
        """Perform search in a specific tab"""
        try:
            driver.switch_to.window(tab_handle)
            
            # Go to Google
            driver.get("https://www.google.com")
            
            # Find search box and search
            search_box = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "q"))
            )
            search_box.clear()
            search_box.send_keys(query)
            search_box.send_keys(Keys.RETURN)
            
            # Wait for results
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "search"))
            )
            
            # Extract top results
            results = []
            try:
                result_elements = driver.find_elements(By.CSS_SELECTOR, "div.g")[:3]  # Top 3 results
                for element in result_elements:
                    try:
                        title_elem = element.find_element(By.CSS_SELECTOR, "h3")
                        link_elem = element.find_element(By.CSS_SELECTOR, "a")
                        snippet_elem = element.find_element(By.CSS_SELECTOR, "span[data-st]")
                        
                        results.append({
                            "title": title_elem.text,
                            "url": link_elem.get_attribute("href"),
                            "snippet": snippet_elem.text
                        })
                    except:
                        continue
            except:
                pass
            
            return {
                "query": query,
                "results": results,
                "tab_title": driver.title,
                "current_url": driver.current_url
            }
            
        except Exception as e:
            return {
                "query": query,
                "error": str(e),
                "results": []
            }
    
    async def _collect_results(self, research_session: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Collect and organize research results"""
        all_results = []
        
        for tab_info in research_session["tabs"]:
            if "result" in tab_info and tab_info["result"].get("results"):
                for result in tab_info["result"]["results"]:
                    all_results.append({
                        "source_query": tab_info["query"],
                        "title": result.get("title", ""),
                        "url": result.get("url", ""),
                        "snippet": result.get("snippet", ""),
                        "relevance_score": self._calculate_relevance(result, research_session["topic"])
                    })
        
        # Sort by relevance
        all_results.sort(key=lambda x: x["relevance_score"], reverse=True)
        
        return all_results
    
    def _calculate_relevance(self, result: Dict[str, Any], topic: str) -> float:
        """Simple relevance scoring based on keyword matches"""
        topic_words = topic.lower().split()
        title = result.get("title", "").lower()
        snippet = result.get("snippet", "").lower()
        
        score = 0.0
        for word in topic_words:
            if word in title:
                score += 2.0  # Title matches are more important
            if word in snippet:
                score += 1.0
        
        return score
    
    async def get_research_status(self) -> Dict[str, Any]:
        """Get status of all research sessions"""
        return {
            "active_sessions": len(self.research_sessions),
            "sessions": {
                sid: {
                    "topic": session["topic"],
                    "tabs": len(session["tabs"]),
                    "runtime": time.time() - session["start_time"]
                }
                for sid, session in self.research_sessions.items()
            }
        }

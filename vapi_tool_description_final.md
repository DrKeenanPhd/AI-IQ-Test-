# VAPI Tool Description (Copy-Paste Ready)

Call this function to capture and sync complete AI IQ assessment results with enhanced voice integration data. This tool captures:

1. **Core AI IQ Analysis**: Overall scores, pain points analysis (4 categories), and context assessments (5 areas)
2. **Voice Integration Data**: Call metadata, conversation highlights, verbal summaries, and transcript insights  
3. **API Tool Usage**: Track which tools were used during analysis and data quality assessment
4. **Subscription Recommendations**: AI IQ Business Analysis and VIP support recommendations with priority levels
5. **Enhanced Report Metadata**: Frontend display optimization and user experience enhancements

The agent should call this function at the end of every AI IQ assessment to ensure all conversation data, analysis results, and recommendations are properly captured and synced to both GHL custom fields and Supabase for the personalized report page.

**Required**: contact_id and session_metadata (with vapi_call_id). All other fields allow dynamic population based on conversation and analysis performed.

**Voice Integration Features**:
- Session metadata captures call duration, agent confidence, and return user status
- Voice summary includes verbal recommendations and conversation highlights
- API data sources track which tools were used and data quality assessment
- Enhanced subscription recommendations with priority levels and ROI timelines

This automatically updates the contact's GHL record and creates their personalized report page at aiiq.aiaugmented.net/report/{contact_id}

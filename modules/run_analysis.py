market_database = download_market_data()
analysis_database = calculate_indicators(market_database)
research_table = build_research_table(analysis_database)
return research_table

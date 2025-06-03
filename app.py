import asyncio
import base64
import json
import os
import pathlib
from typing import AsyncGenerator, Literal

import gradio as gr
import numpy as np
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastrtc import (
    AsyncStreamHandler,
    Stream,
    get_cloudflare_turn_credentials_async,
    wait_for_item,
)
from google import genai
from google.genai.types import (
    LiveConnectConfig,
    PrebuiltVoiceConfig,
    SpeechConfig,
    Content,
    VoiceConfig,
)
from gradio.utils import get_space
from pydantic import BaseModel

current_dir = pathlib.Path(__file__).parent

load_dotenv()



rtc_configuration = {
    "iceServers": [
        {
            "urls": "turn:3.86.17.131:80",
            "username": "vaishnavik",
            "credential": "Gajanan@130599"
        },
    ]
}



sys_instruct = Content(parts=[{"text": 
                               

 """You are helful HR assitstnat. Your name is BATMAN. Please use english as default language. You represetnt Alpha TECH lab and related HR team. You will answer any questions from provided context with positivity. Any negative comments should be responded with positiveness. Respond with referenece to following manuals.                           

 You are an multilingual help HR assistant, Answer user queries in any language. For any queries not related to provided content, Positively deny answering. Help users to provide positive and meaningful feedback.
 #  Please refer following document for answering user queries. In case of critical query, ask user to connect with HR team for help.


# Standard Policy Document: Rewards and Recognition Policy                                                    
 
# 1                                           Copyright@2024 Alpha TECH Lab and/ or Alpha TECH as applicable. All rights reserved.                              Private & Confidential 
 
# Alpha TECH Technologies Private Limited 
# (Alpha TECH Software Laboratory Private Limited is merged into Alpha TECH Technologies Private Limited 
# vide National Company Law Tribunal (NCLT) order) 
 
# Registered Office: New No. 13 (Old No. 11), Rajiv Gandhi Salai (OMR) Sholinganallur, Kancheepuram, 
# Chennai - 600 119, Tamil Nadu. Tel: +91 44 6669 4287 
# Pune Office: 8th Floor (A and B), Amar Arma Genesis, Baner Road, Pune – 411 045 
# Tel: +91 020 6310 6500 / 020 6310 6600 
# CIN No: U72200TN2007PTC062974 | www.Alpha TECHtech.com , www.Alpha TECHlab.com 
 
# Rewards and Recognition Policy 
 


# Standard Policy Document: Rewards and Recognition Policy                                                    
 
# 2                                           Copyright@2024 Alpha TECH Lab and/ or Alpha TECH as applicable. All rights reserved.                              Private & Confidential 
 

# Standard Policy Document: Rewards and Recognition Policy                                                    
 
# 3                                           Copyright@2024 Alpha TECH Lab and/ or Alpha TECH as applicable. All rights reserved.                              Private & Confidential 
 
 
# CONTENTS 
# 1. Objective ….……………………………………………………………………………………………….……………………… 4 
# 2. Purpose.….………………………………………………………………………………………………………….…………….. 4 
# 3. Scope………………………………………………………………………………………………………………….…………….. 4 
# 4. Policy……………………………………………………..……………………………….………………………….…………….. 4 
# 4.1 Quarterly Awards……………………………..………………………………………………………….……………..  4 
# 4.1.1 Star Performer of the Quarter……………………………………………………………………………. 4 
# 4.1.2 Star Team of the Quarter…………………………………………………………………………………… 5 
# 4.2 SPOT Recognition Program………………………………………………………………………………………….. 5  
# 4.3 Loyalty Awards…………………………………………………………………………………………………………….. 7 
# 5. Review and Revision……………….……………………………………………………………………….………………… 7 
 



# Standard Policy Document: Rewards and Recognition Policy                                                    
 
# 4                                           Copyright@2024 Alpha TECH Lab and/ or Alpha TECH as applicable. All rights reserved.                              Private & Confidential 
 
# 1. Objective 
# The objective of this policy is to recognize and reward the contributions of Alpha TECH Lab | Alpha TECH 
# employees. This encourages high performance, customer delight, and adherence to company 
# values and culture which promotes a healthy, cohesive workplace. 
# 2. Purpose 
# The purpose of the Rewards & Recognition Program is to: 
# • Align all employees with the organization's rewards and recognition framework. 
# • Motivate employees by acknowledging their achievements and contributions. 
# • Foster a culture of appreciation and recognition. 
# • Enhance employee engagement and retention. 
# • Encourage exemplary performance and teamwork. 
# 3. Scope 
# This policy applies to all employees within the Alpha TECH Lab| Alpha TECH. 
# 4. Policy:  
# 4.1 Quarterly Awards: 
 
# The Quarterly Awards at Alpha TECH Lab | Alpha TECH are designed to recognize and reward employees and 
# teams for their exceptional performance and contributions every quarter. These awards aim to 
# encourage continuous excellence and reinforce a culture of recognition within the organization. 
 
# These awards apply to all full-time employees and Retainers within Alpha TECH Lab| Alpha TECH. 
 
# Selection Process: 
# Each vertical, department will have the awards committee, whose responsibility is to select the 
# most qualifying individuals against the reward criteria set for the award category.   
# 4.1.1 Star Performer of the Quarter: 
# Star award is named to acknowledge the special contribution made by an individual to create 
# significant business impact, Customer Delight, Process improvement, and exceptional 
# contribution. 


# Standard Policy Document: Rewards and Recognition Policy                                                    
 
# 5                                           Copyright@2024 Alpha TECH Lab and/ or Alpha TECH as applicable. All rights reserved.                              Private & Confidential 
 
# Reward Type 
# Nomination From 
# Selection Panel 
# ➢ Cash Reward 
# ➢ Trophy 
# ➢ Certificates 
# BU Head/ CSM/ Manager 
# Internal Committee (Delivery 
# Head, Delivery Head inline & 
# respective HRBP) 
# 4.1.2 Star Team of the Quarter: 
# The award is extended to the best team that has demonstrated outstanding client delivery, a high 
# level of collaboration within and between teams, and achieved team goals through exemplary 
# collective efforts with minimum disruptions during the quarter. 
# Reward Type 
# Nomination From 
# Selection Panel 
# ➢ Cash Reward 
# ➢ Trophy 
# ➢ Certificates 
# BU Head/ CSM/ Manager 
# Internal Committee (Delivery 
# Head, Delivery Head inline & 
# respective HRBP) 
 
# An E-certificate and cash reward as follows will be accorded to the winner: 
# Team Size 
# Cash Rewards 
# <5 members 
# INR 1,200/ Head 
# 5–10 Members team 
# INR 1,200/ Head 
# 10-15 Members team 
# INR 1,200/ Head 
# >15 Member Team 
# INR 18000 Max 
 
# 4.1.3 Customer Delight: 
# The Customer Delight Award is granted to individuals who deliver exceptional impact, business value, 
# and superior service experiences, significantly exceeding client expectations. This recognition 
# celebrates those who elevate customer satisfaction and loyalty through outstanding performance 
# leaving an impactful experience in the mind of the customer. 
# Reward Type 
# Nomination From 
# Selection Panel 
# ➢ Cash Reward 
# ➢ Trophy 
# ➢ Certificates 
# BU Head/ CSM/ Manager 
# Level 1 – Internal Committee 
# (Delivery Head, Delivery Head 
# inline & respective HRBP) 
 
# Level 2 – Panel Discussion 
 
# 4.2 Long Service Awards 
# Long service awards are key milestone awards for employees for their loyalty, commitment to the 
# organization vision and growth journey. These awards are on completion of 5, 10, 15, 20 & 25 year 


# Standard Policy Document: Rewards and Recognition Policy                                                    
 
# 6                                           Copyright@2024 Alpha TECH Lab and/ or Alpha TECH as applicable. All rights reserved.                              Private & Confidential 
 
# milestone and would be honored with a Service plaque and reward as follows: 
 
 
# Description 
# Reward 
# 5 Years of Service 
# Lenovo Tablet / Amazon Alexa 
# 10 and above Years of Service 
# Thomas Cook Travel Voucher / Gold voucher 
 
# 4.3 SPOT Recognition 
 
# SPOT Recognition Program will recognize spontaneous contributions that are impactful and towards 
# organization initiatives, brand building and fostering a positive work culture. 
 
# The program is based on nomination by self, manager, peers, seniors, and any other stakeholder. 
# The recognition is awarded based on the nomination and approval of the contribution by respective 
# Stakeholder followed by HR Business Partner. 
 
# These awards apply to all the full-time employees, retainers and contractors. 
 
# An E – certificate and points will be awarded to the winner. Points will be converted to reward as 
# follows. Various categories of recognition along with points are stated below. 
# Category 
# Metric 
# Description 
# Points* 
# 4.3.1 Above & Beyond 
# Above & Beyond 
# Above & Beyond is rewarded to acknowledge the 
# extra effort of the individuals who goes extra mile 
# on areas such as Process Improvement, Escalation 
# management, Client management, Reduction in 
# TAT. The nominations will be received from BU 
# Head/ CSM/ Manager which will be approved by 
# respective HRBP. 
# 1,000 
# 4.3.2 Organizational 
# Initiatives 
# Conducting 
# Training – 
# 8 Hours / A Day 
# This is rewarded to those who invests their own 
# time in training others 
# 2,000 
# Hiring – 
# Weekend Drives 
# This is for employees who goes extra mile and 
# compromise their family and personal time to get 
# best recruits from the industry/market 
# 2,000 


# Standard Policy Document: Rewards and Recognition Policy                                                    
 
# 7                                           Copyright@2024 Alpha TECH Lab and/ or Alpha TECH as applicable. All rights reserved.                              Private & Confidential 
 
# *Amount associated with G-Points will be credited though Sodexo (Multi-benefit Sodexo Card) 
 
 
# 4.3.3 Culture & Camaraderie 
 
# The recognition program honors employees who exemplify our company values and foster a 
# positive work culture. This non-monetary program includes below mentioned cards promoting 
# appreciation, camaraderie, and learning from mistakes. 
 
# • Value Card (RITE) 
# • Thank you, Card 
# • Pat on The Back (Well Done) 
# • Sorry Card 
 
# 5 Review and Revision 
# This policy will be reviewed periodically to ensure its effectiveness and relevance. Any necessary 
# revisions will be made in consultation with relevant stakeholders and approved by senior 
# management. 
 
 
# External Seminars 
# Representing  
#  (Speaking, 
# Publication) 
# This is rewarded to those who do an external 
# branding by promoting Alpha TECH Lab | Alpha TECH in other 
# public forums. 
# 2,000 
# Engage - Blog’s, 
# Articles 
# This is rewarded to those who write an excellent 
# blog/article in Engage Magazine/Vibe. 
# 1,000 
# Audit & 
# Compliances 
# Quality Team will only have access to nominate 
# employees for this reward. This reward is given to 
# employees for not just championing compliance 
# but ensure with Zero NC and providing accurate 
# data for all audits to ensure the project/ function 
# is Error free. 
# 1,000 

 
 
# Holiday List for  
# Global        Locations - 2025 
 
# • • • • 
#  Human Resources 


# Published Holiday’s – Global Locations 
# 2 
# Copyright © 2023 Alpha TECH Lab and / or Alpha TECH as applicable. All rights reserved. 
# Private & Confidential 
 
 
 
 
 
 
# Contents 
# Foreword .......................................................................................................... 3 
# Chennai ............................................................................................................. 4 
# Pune & Vadodara .............................................................................................. 5 
# United States of America ................................................................................... 6 
# United Kingdom ................................................................................................ 7 
# United Arab Emirates ....................................................................................... 8 
# Oman ............................................................................................................... 9 


# Published Holiday’s –Global Locations 
# 3 
# Copyright © 2023 Alpha TECH Lab and / or Alpha TECH as applicable. All rights reserved. 
# Private & Confidential 
 
 
 
 
 
 
 
# FOREWORD: 
 
# The listed holidays reflect a careful consideration of traditions observed across 
# our various locations globally. We acknowledge and respect the unique customs 
# and celebrations embraced by our colleagues worldwide. 
 
# While this document provides a clear framework, it is not exhaustive. Should you 
# have any specific questions regarding individual holidays, leave policies, or any 
# other aspect of holiday observance, we encourage you to reach out to your 
# dedicated HR Business Partner (HRBP). They are a valuable resource and will be 
# happy to assist you with navigating your individual circumstances. 
 
# Alpha TECH Lab | Alpha TECH is committed to fostering a supportive and inclusive environment 
# that recognizes the importance of personal well-being and cultural appreciation. 
 
 
 
# Sincerely,  
# Leadership Team 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 


# Published Holiday’s –Global Locations 
# 4 
# Copyright © 2023 Alpha TECH Lab and / or Alpha TECH as applicable. All rights reserved. 
# Private & Confidential 
 
 
 
 
 
#                                                   India 
# Chennai:  
 
 
# S. No. 
# Date 
# Day 
# Holiday Description 
# 1 
# 01-Jan-25 
# Wednesday 
# New Years Day 
# 2 
# 14-Jan-25 
# Tuesday 
# Pongal 
# 3 
# 31-Mar-25 
# Monday 
# Ramzan (Idu'l Fitr) 
# 4 
# 14-Apr-25 
# Monday 
# Tamil New Year 
# 5 
# 01-May-25 
# Thursday 
# May Day 
# 6 
# 15-Aug-25 
# Friday 
# Independence Day 
# 7 
# 02-Oct-25 
# Thursday 
# Gandhi Jayanthi/Dussehra 
# 8 
# 20-Oct-25 
# Monday 
# Diwali Festival 
# 9 
# 25-Dec-25 
# Thursday 
# Christmas Day 
# Floating Holidays to Choose From 
# In addition to the above-mentioned holidays, employees can avail 2 optional holiday (Two for 
# the year) from the below given holidays. 
# 1 
# 14-Mar-25 
# Friday 
# Holi 
# 2 
# 18-Apr-25 
# Friday 
# Good Friday 
# 3 
# 27-Aug-25 
# Thursday 
# Ganesh Chaturthi 
# 4 
# 05-Sep-25 
# Friday 
# Milad-un-Nabi 
# 5 
# 01-Oct-25 
# Wednesday 
# Ayutha Pooja 
# 6 
# 21-Oct-25 
# Tuesday 
# Diwali (Laxmi Pooja) 
# Employees deputed at the client location will follow the holiday list as per the client organization. 


# Published Holiday’s –Global Locations 
# 5 
# Copyright © 2023 Alpha TECH Lab and / or Alpha TECH as applicable. All rights reserved. 
# Private & Confidential 
 
 
 
 
 
 
# Pune & Vadodara: 
 
 
# S. No. 
# Date 
# Day 
# Holiday Description 
# 1 
# 01-Jan-25 
# Wednesday 
# New Years Day 
# 2 
# 14-Mar-25 
# Friday 
# Holi 
# 3 
# 31-Mar-25 
# Monday 
# Ramzan (Idu'l Fitr) 
# 4 
# 01-May-25 
# Thursday 
# May Day 
# 5 
# 15-Aug-25 
# Friday 
# Independence Day 
# 6 
# 27-Aug-25 
# Wednesday 
# Ganesh Chaturthi 
# 7 
# 02-Oct-25 
# Thursday 
# Gandhi Jayanthi/Dusshera 
# 8 
# 21-Oct-25 
# Tuesday 
# Diwali Festival  
# 9 
# 25-Dec-25 
# Thursday 
# Christmas Day 
# Floating Holidays to Choose From 
# In addition to the above-mentioned holidays, employees can avail 2 optional holiday (Two for 
# the year) from the below given holidays. 
# 1 
# 14-Jan-25 
# Tuesday 
# Makar Sankranti/Uttar Ayaan 
# 2 
# 26-Feb-25 
# Wednesday 
# Maha Shivaratri 
# 3 
# 18-Apr-25 
# Friday 
# Good Friday 
# 4 
# 05-Sep-25 
# Friday 
# Milad-un-Nabi 
# 5 
# 22-Oct-25 
# Wednesday 
# Diwali (Padwa) 
# 6 
# 05-Nov-25 
# Friday 
# Guru Nanak Jayanti 
# Employees deputed at the client location will follow the holiday list as per the client organization. 


# Published Holiday’s – Global Locations 
# 6 
# Copyright © 2023 Alpha TECH Lab and / or Alpha TECH as applicable. All rights reserved. 
# Private & Confidential 
 
 
 
 
# United States of America: 
 
 
# S. No. 
# Date 
# Day 
# Holiday Description 
# 1 
# 01-Jan-25 
# Wednesday 
# New Year’s Day 
# 2 
# 26-May-25 
# Monday 
# Memorial Day 
# 3 
# 19-Jun-25 
# Thursday 
# Juneteenth Day 
# 4 
# 04-Jul-25 
# Friday 
# Independence Day 
# 5 
# 01-Sep-25 
# Monday 
# Labor Day 
# 6 
# 27-Nov-25 
# Thursday 
# Thanksgiving 
# 7 
# 28-Nov-25 
# Friday 
# Day after Thanksgiving 
# 8 
# 25-Dec-25 
# Thursday 
# Christmas Day 
# Floating Holidays to Choose (Pro-Rated on Start Date) 
# In addition to the above-mentioned holidays, employees can avail 3 optional holidays (Three for the 
# year) from the below given holidays. 
# 1 
# 20-Jan-25 
# Monday 
# Martin Luther King Day 
# 2 
# 17-Feb-25 
# Monday 
# Washington's Birthday (Presidents' Day) 
# 3 
# 18-Apr-25 
# Friday 
# Good Friday 
# 4 
# 13-Oct-25 
# Monday 
# Columbus Day 
# 5 
# 21-Oct-25 
# Tuesday 
# Diwali 
# 6 
# 11-Nov-25 
# Tuesday 
# Veterans Day 
# 7 
# 24-Dec-25 
# Wednesday 
# Christmas Eve 
# Employees deputed at the client location will follow the holiday list as per the client organization 


# Published Holiday’s – Global Locations 
# 7 
# Copyright © 2023 Alpha TECH Lab and / or Alpha TECH as applicable. All rights reserved. 
# Private & Confidential 
 
 
 
# United Kingdom: 
 
# S. No. 
# Date 
# Day 
# Holiday Description 
# 1 
# 01-Jan-25 
# Wednesday 
# New Years Day 
# 2 
# 18-Apr-25 
# Friday 
# Good Friday 
# 3 
# 21-Apr-25 
# Monday 
# Easter Monday 
# 4 
# 05-May-25 
# Monday 
# Early May Bank Holiday 
# 5 
# 26-May-25 
# Monday 
# Spring Bank Holiday 
# 6 
# 25-Aug-25 
# Monday 
# Summer Bank Holiday 
# 7 
# 21-Oct-25 
# Tuesday 
# Diwali 
# 8 
# 25-Dec-25 
# Thursday 
# Christmas 
# 9 
# 26-Dec-25 
# Friday 
# Boxing Day 
# In addition to the above-mentioned holidays, employees can avail 2 optional holiday (Two for the 
# year) from the below given holidays. 
# 1 
# 27-Aug-25 
# Wednesday 
# Ganesh Chaturthi 
# 2 
# 02-Oct-25 
# Thursday 
# Gandhi Jayanthi/Dussehra 
# 3 
# 22-Oct-25 
# Wednesday 
# Diwali (Padwa) 
 
 
 
 
 
 
 
 
 
 
 
 


# Published Holiday’s – Global Locations 
# 8 
# Copyright © 2023 Alpha TECH Lab and / or Alpha TECH as applicable. All rights reserved. 
# Private & Confidential 
 
 
 
 
# United Arab Emirates: 
 
 
# Sr. No 
# Date 
# Day 
# Holiday Description 
# 1 
# 01-Jan-25 
# Wednesday 
# New Year's Day 
# 2 
# 29 Mar 2025 to 01 
# Apr 2025 
# Saturday to Tuesday 
# Eid al-Fitr Holiday* 
# 3 
# 05-Jun-25 
# Thursday 
# Arafat Day 
# 4 
# 07 Jun 2025 & 08 
# Jun 2025 
# Saturday & Sunday 
# Eid al-Adha 
# 5 
# 26-Jun-25 
# Thursday 
# Islamic New Year* 
# 6 
# 04-Sep-25 
# Thursday 
# Prophet Muhammad's Birthday* 
# 7 
# 02-Dec-25 
# Tuesday 
# National Day 
# 8 
# 03-Dec-25 
# Wednesday 
# National Day Holiday 
# *These are tentative dates since the date may change depending on sighting of the 
# crescent. 
# Employees deputed at the client location will follow the holiday list as per the client 
# organization 


# Published Holiday’s – Global Locations 
# 9 
# Copyright © 2023 Alpha TECH Lab and / or Alpha TECH as applicable. All rights reserved. 
# Private & Confidential 
 
 
 
 
 
# Oman: 
 
# Sr. No 
# Date 
# Day 
# Holiday Description 
# 1 
# 01-Jan-25 
# Wednesday 
# New Year's Day 
# 2 
# 27-Jan-25 
# Monday 
# The Prophet's Ascension Day* 
# 3 
# 29 Mar 2025 to 01 
# April 2025 
# Saturday to Tuesday 
# Eid al-Fitr Holiday* 
# 4 
# 05 Jun 2025 to 09 
# Jun 2025 
# Thursday to Monday 
# Eid al-Adha* 
# 5 
# 26-Jun-25 
# Thursday 
# Islamic New Year 
# 6 
# 04-Sep-25 
# Thursday 
# Prophet Muhammad's Birthday* 
# 7 
# 18-Nov-25 
# Tuesday 
# National Day 
# 8 
# 19-Nov-25 
# Wednesday 
# National Day 
# *These are tentative dates since the date may change depending on sighting of the 
# crescent. 
# Employees deputed at the client location will follow the holiday list as per the client 
# organization 
 


#  Guideline –  Insurance Policies 
# Alpha TECH Technologies                                                                Alpha TECH Internal                                     
#  Page 1 of 8 
 

 
 
# Alpha TECH Technologies Private Limited 
# (Alpha TECH Software Laboratory Private Limited is merged into Alpha TECH Technologies 
# Private Limited 
# vide National Company Law Tribunal (NCLT) order) 
 
# Registered Office: New No. 13 (Old No. 11), Rajiv Gandhi Salai (OMR) Sholinganallur, Kancheepuram, 
# Chennai - 600 119, Tamil Nadu. Tel: +91 44 6669 4287 
# Pune Office: 8th Floor (A and B), Amar Arma Genesis, Baner Road, Pune – 411 045 
# Tel: +91 020 6310 6500 / 020 6310 6600 
# CIN No: U72200TN2007PTC062974 | www.Alpha TECHtech.com , www.Alpha TECHlab.com 
# Guideline – Insurance Policies 


#  Guideline –  Insurance Policies 
# Alpha TECH Technologies                                                                Alpha TECH Internal                                     
#  Page 2 of 8 
 
 
 
# Table of Contents 
 
# 1. Introduction………………………………………………………………...………………………………3 
# 2. Scope & Applicability………………………………………………………………...…………………3 
# 3. High Level Overview of the Process………………………………………………………………3 
# 4. Systems & inputs Required………………………………………………………………...…………4 
# 5. Responsibility Matrix………………………………………………………………...………………….4 
# 6. Service Level Agreement ………………………………………………………………...……………5 
# 7. Guidelines ………………………………………………………………...…………………..................5 
# 8. Policy wise Insurance Providers & TPA information……………………………………….6 
# 9. GMC & GPAP Forms & Network List ………………………………………………………………7 
# 10. Escalation & Communication Matrix……………………………………………………………….7 
# 11. Change History………………………………………………………………...…………………............8 
 
 


#  Guideline –  Insurance Policies 
# Alpha TECH Technologies                                                                Alpha TECH Internal                                     
#  Page 3 of 8 
 
# 1. Introduction 
# This Standard Operating Procedure details the step-by-step approach for Insurance Process and 
# proceedinAlpha TECH. This document is recommended to be used as the main reference document for HR 
# which outlines the complete Insurance procedure and maintain and track the changes to the main 
# process, if any. 
# 2. Scope & Applicability 
# ✓ The insurance Coverage from the date of joining is to be extended to all the employees 
# who are part of Alpha TECH India  
# ✓ Periodical Activities, Timelines and Compliance ProceedinAlpha TECH 
# ✓ Benefit benchmarking with the Industry practices at the time of Insurance renewal 
 
# 2.1 
# Policies in effect 
 
# ✓ Group Mediclaim Policy (GMC) 
# ✓ Group Personal Accident Policy (GPAP) 
# ✓ Group Term Life Insurance (GTLP) 
 
# 2.2 
# Coverage Extended to  
# ✓ GMC (Employee + Spouse (if applies) + up to Two Children) 
# ✓ GMC Parents / In Laws can be covered and the employee to bear the premium for the 
# coverage 
# ✓ Top-up options are available 
# ✓ GPA (All Employees) 
# ✓ GTL (All Employees) 
# 3. High Level Overview of the Process 
 
# STEP 1: Collate the information provided by the employee at the time of Joining for new additions 
# and derive the employee exits from the HRMS portal in the form of report for deletion input. Input on 
# employee Transfers is to be sought from the payroll team and processed as appropriate  
 
# STEP 2: Prepare the input file with the addition and deletion inputs in the format prescribed by the 
# Vendor 
 
# STEP 3: The input prepared must be sent to the Vendor on a fortnightly / monthly basis for 
# endorsements processing  
 
# STEP 4: Follow up with the vendor for the addition and deletion endorsement 
 
# Step 5: Monthly review for the CD Balance check, endorsements and other process related updates 


#  Guideline –  Insurance Policies 
# Alpha TECH Technologies                                                                Alpha TECH Internal                                     
#  Page 4 of 8 
 
# 4. Systems & inputs Required 
 
# ✓ New Joiners Information from the HRMS Portal (Darwin Box) 
# ✓ Employee Exit Information from the HRMS Portal (Darwin Box) 
# ✓ Medi assist TPA Online Portal – for status updates, Insurance e-Cards and claim deficiency 
# related information and Claim forms  
# ✓ E-mail IDs’ used – HR-Ops, HR Communications 
 
# 5. Responsibility Matrix 
 
# Transaction Type 
# Duration 
# Responsibility 
# Inputs  
# GMC Addition & Deletion 
# Monthly 
# HR Operations team  
# GPAP & GTL - Addition & 
# Deletion 
# Monthly 
# HR Operations team  
# Reporting a Death Claim 
# As and when required 
# (within 30 Days from the 
# day of the accident / 
# Incident) 
# Respective HR Business Partners 
# GMC, GPA & GTL Claims 
# As and when required 
# HR Operations team  
# Tickets, Query handling & Support 
# As and when required 
# HR Operations team  
# Claim Status Follow-up & Other Support 
# required 
# As and when required 
# HR Operations team  
# Premium & CD Balance Check 
# Monthly 
# HR Operations team  
 
# 6. Service Level Agreement  
 
# The SLA for a response to a query raised with a ticket in the portal or with an email is listed below: 
# • 
# The claim forms need to be submitted within the SLA’s defined in the checklist in the annexure 
# and forms will be forwarded to the insurance company within 2 working days from the date 
# of receipt of the forms 
 
# • 
# The reimbursement Claim settlement will take a minimum of 20 Calendar Days approximately 
# and further delays can be expected if document insufficiencies are encountered 
 
 


#  Guideline –  Insurance Policies 
# Alpha TECH Technologies                                                                Alpha TECH Internal                                     
#  Page 5 of 8 
 
# 7. Guidelines  
 
# 7.1 Group Mediclaim Policy  
# • 
# Employees can avail Cashless Claim facility if the treatment procedure is planned, provided it 
# meets the following criterions  
 
# a. The hospital in which the treatment is undertaken should be a listed network 
# hospital as per the list shared by the insurance company / TPA 
# b. Notification in advance is to be given to the insurance desk of the respective 
# hospital where the treatment / maternity is planned for pre-authorization 
# • 
# Mid-term inclusion inputs from the employee is not permitted unless there is a life event 
# (Marriage, Birth, Demise or Divorce) 
# • 
# Exceptions of any kind should be permitted only with the approval from Head of HR with 
# appropriate justifications 
# • 
# Notification within 48 hours from the time of admission is to be given to the Insurance 
# Provider / TPA any hospitalization if it is not emergency in nature   
# • 
# Reimbursement claims beyond 30 Days from the date of discharge may not be processed by 
# the insurance company 
 
# 7.2 Group Personal Accident Policy (GPAP) 
# • 
# This insurance coverage is extended to all the employees and it covers any ailments caused 
# because of an accident  
# • 
# This coverage is extended only to the employees and their dependents are not covered 
# • 
# All the claims will be reimbursement claims in nature and the claim intimation should be made 
# within 2 weeks from the date of the incident / accident 
# • 
# Death of an employee should be reported to the insurance company / TPA within 30 days 
# from the date of the incident / accident 
# • 
# Reimbursement claims beyond 30 Days from the date of discharge / date of the event may 
# not be processed by the insurance company 
# • 
# In the event of a demise of an employee, the nominees (as per the nomination given by the 
# employee) may claim the benefit with the required supporting documents as appropriate. 
 
# 7.3 Group Term Life Insurance Policy 
# • 
# This policy covers the demise of an employee under any circumstance 
# • 
# Death of an employee should be reported to the insurance company / TPA within 30 days 
# from the date of the incident / accident 
# • 
# In the event of a demise of an employee, the nominees (as per the nomination given by the 
# employee) may claim the benefit with the required supporting documents as appropriate. 


#  Guideline –  Insurance Policies 
# Alpha TECH Technologies                                                                Alpha TECH Internal                                     
#  Page 6 of 8 
 
 
# 7.4 Policy wise Sum Insured Information 
# Sl. No 
# Policy 
# Grade 
# Sum Insured 
# 1 
# GMC 
# All Employees(E+S+2C) 
# INR 5,00,000/-  
# 2 
# GPAP 
# E 
# INR 15,00,000/- 
# 3 
# T 
# INR 20,00,000/- 
# 4 
# M, S & Executive Band 
# INR 25,00,000/- 
# 5 
# GTL 
# All Employees 
# INR 25,00,000/- 
# *Parental policy sum insured of INR 3,00,00/- and top up options of 2 Lakhs, 4 Lakhs, 6 Lakhs, 8 Lakhs 
# and 10 Lakhs – For these mentioned voluntary options, the premium will be borne by the employee 
# 8.  Policy wise Insurance Providers & TPA information 
# Sl. No. 
# Policy 
# Insurance Provider 
# TPA 
# Broker Firm 
# 1 
# GMC 
# Oriental Insurance 
# Medi Assist 
# Neo Insurance Brokers 
# 2 
# GPAP 
# Sundaram 
# General 
# Insurance 
# NA 
# Neo Insurance Brokers 
# 3 
# GTL 
# Adithya Birla Capitals 
# NA 
# Neo Insurance Brokers 
 
 
# 9. Escalation & Communication Matrix 
 
# 9.1 
# Escalation Matrix 
 
# Sl. No 
# Issue 
# Primary Contact 
# Secondary Contact 
# 1 
# Hospitalization 
 
# HR Operations team (Linu > Sandra) 
# 2 
# GPAP 
# 3 
# GTL 
 
# 9.2 
# Communication Matrix 
# Sl. 
# No 
# Description 
# Policy 
# To Whom 
# Frequency 
# Medium 
# 1 
# Claim intimation in case of 
# a claim 
# All 
# Policies 
# To the TPA / Insurance 
# Company / HR Spoc 
# As and when 
# required 
# E-Mail 
 


#  Guideline –  Insurance Policies 
# Alpha TECH Technologies                                                                Alpha TECH Internal                                     
#  Page 7 of 8 
 
# 9.3 
# Scheduled Communication 
# Sl. 
# No 
# Description 
# Who 
# Whom 
# Medium 
# 1 
# Communication emails on Coverage and Enrolment 
# HR 
# To all India Employees 
# E-Mail 
 
# 9.3.1 
# Unscheduled Communication 
# Sl. 
# No Description 
# Who Whom 
# Medium 
# 1 
# Any important update on Change in Policy 
# HR 
# To all India Employees E-Mail 
 
 

 
# Alpha TECH Technologies Private Limited 
# (Alpha TECH Software Laboratory Private Limited is merged into Alpha TECH Technologies Private Limited 
# vide National Company Law Tribunal (NCLT) order) 
 
# Registered Office: New No. 13 (Old No. 11), Rajiv Gandhi Salai (OMR) Sholinganallur, Kancheepuram, 
# Chennai - 600 119, Tamil Nadu. Tel: +91 44 6669 4287 
# Pune Office: 8th Floor (A and B), Amar Arma Genesis, Baner Road, Pune – 411 045 
# Tel: +91 020 6310 6500 / 020 6310 6600 
# CIN No: U72200TN2007PTC062974 | www.Alpha TECHtech.com , www.Alpha TECHlab.com 

 
# Contents 
 
# PART I – About Us .............................................................................................................. 5 
# Code of Conduct and Ethics................................................................................................ 6 
# Hiring ................................................................................................................................... 6 
# Employee Experience ......................................................................................................... 6 
# Candidate Experience ......................................................................................................... 6 
# Onboarding Process ............................................................................................................ 7 
# SHEroes .............................................................................................................................. 8 
# Business Etiquette ............................................................................................................... 8 
# Dining Etiquette: .................................................................................................................. 9 
# Identity Cards ...................................................................................................................... 9 
# Working Days ...................................................................................................................... 9 
# Office hours ....................................................................................................................... 10 
# Women employees working after 8:00 PM ....................................................................... 10 
# Time Tracking .................................................................................................................... 10 
# Holidays ............................................................................................................................. 10 
# Workplace Cleanliness ...................................................................................................... 10 
# Hardware and Software ..................................................................................................... 10 
# Security .............................................................................................................................. 10 
# Visitors ............................................................................................................................... 11 
# Visiting Cards .................................................................................................................... 11 
# Network Access Agreement .............................................................................................. 11 
# Proprietary Rights and Non-Disclosure Agreement .......................................................... 11 
# Part II – Your Entitlement ...................................................................................................... 12 
# Leave Policy: ..................................................................................................................... 12 
# Employee Wedding& New-born Gift ................................................................................. 14 
# Night Shift Allowance ........................................................................................................ 14 
# On-Call Allowance ............................................................................................................. 14 
# Team Lunch/Dinner Reimbursement ................................................................................ 15 
# Business Travel Policy ...................................................................................................... 15 
# Kit Allowance ..................................................................................................................... 16 
# Provident Fund .................................................................................................................. 16 
# Insurance Coverage .......................................................................................................... 16 
# Transfers ................................................................................................................................ 17 
# Separations ............................................................................................................................ 17 
# 1. 
# Voluntary Separation ................................................................................................. 17 
# 2. 
# Involuntary Separation .............................................................................................. 17 
# Leave during Notice period ............................................................................................... 18 
# Retirement ......................................................................................................................... 19 
# Part III – Organization Growth and Employee Development ................................................ 19 
# Performance Management Programme ............................................................................ 19 
# Performance Improvement Plan Process ......................................................................... 20 
# Career Path / Tracks, Grades & Designations .................................................................. 20 
# Annual Compensation Review .......................................................................................... 20 
# Rewards and Recognitions ............................................................................................... 21 
# Training and Development ................................................................................................ 22 
# Part IV– POSH (Prevention of Sexual Harassment) ............................................................. 24 
# Part V – Our Expectations from You ..................................................................................... 25 
# Annexure-I   Network Security and Usage Policy ................................................................. 25 
# Annexure II - Proprietary Rights and Non-Disclosure Agreement ........................................ 28 


 
 
# Annexure – III - Declaration form by women Employees Leaving Office Premises after 
# 8p.m. ...................................................................................................................................... 31 
# Annexure IV – Business Travel ............................................................................................. 32 
 


 
 
# 5 
 
 
 
 
 
# PART I – About Us 
# Our Vision   
# To galvanize a sense of measurable success in all our client engagements through our committed teams and innovative 
# solutions. 
# Our Mission                                                                                                                                                                    
# To achieve our business goals through an environment that fosters Respect for Individuals, Integrity, Trust and Empathy 
# towards our employees, client, and stakeholders with an obsessive focus on creating disruptive IP-led solutions. 
# Our Value statement  
# Alpha TECH’ RITE forms our core values that is ingrained in the system, it forms the backbone of our internal and 
# external interactions. RITE forms the Alpha TECH DNA. 
# R – Respect & Responsiveness 
# I - Integrity & Innovation 
# T - Teamwork & Trustworthy 
# E - Empathy & Engaging                                          
# Our Quality Policy: Excellence is Our Aim 
# Our vision is to be recognized as a centre of excellence for quality, with a team that reflects high process maturity. We're on 
# a mission to train our employees in quality practices, empowering them to become highly competent resources who drive 
# success for our clients and for Alpha TECH. 
# Our quality program is designed to equip employees with the knowledge and skills they need to excel in their roles, tackle 
# complex problems, and uphold world-class standards. Through continuous learning and development, we're building a team 
# that sets the bar high and strives to clear it. 
# Our Security Policy: Your Trust is Our Priority 
# As a Gartner-rated company with a decade of specialization in security services, Alpha TECH is a trusted partner for organizations 
# seeking comprehensive security solutions. Our services encompass assessment and audit, security testing, and managed 
# security services, all delivered through our state-of-the-art Security Operations Center (SOC) and backed by SIEM tools 
# expertise and ISO-certified processes. We're dedicated to protecting our clients' sensitive information and business assets, 
# with robust systems and strict controls in place to ensure secure access, storage, and transmission. Our commitment to  


 
 
# 6 
 
 
# security means our clients can have confidence that their data is safe with us, their operations will run uninterrupted, and 
# their trust will be earned and upheld. 
# Code of Conduct and Ethics (Annexure) 
# This policy outlines the expected standards of behaviour for all employees of Alpha TECH. As an employee, it is important to 
# adhere to these standards both within the organization and in any external representation of Alpha TECH. Throughout your 
# employment, you are expected to perform your duties efficiently, honestly, faithfully, and to the best of your ability, 
# continuously striving to improve your performance.  
# Applicability 
# This policy applies to all employees, including board members, interns, retainers, consultants, contractors, and any other 
# personnel associated with Alpha TECH. 
# Hiring  
# We follow the philosophy of Hire to Rehire, which speaks for our intent and commitment to the prospective candidates, 
# colleagues and alumni. Our SWAT framework (Smart, Hardworking, Articulate, Technologically curious) forms the core of 
# our hiring philosophy and shapes our recruitment strategy.  We hire extensively partnering with educational 
# institutions/universities ensuring we onboard young talent that immerses with our organizational values thereby creating a 
# whole new line of future leaders at Alpha TECH Lab | Alpha TECH. Candidates are selected based on SWAT philosophy irrespective of age, 
# gender, generation, and are assessed for technical, and cultural fit. Thus, the match between a candidate and the 
# organization is based on shared values. This enables us to measure the candidate’s potential to align with our vision.  
# With our commitment to building a better workplace for our women colleagues, we started our gender diversity initiative 
# that focuses on hiring and inducting more women from campus, lateral and through ‘Restart Program’. The Restart Program 
# focuses on inviting applications exclusively from women who had taken break from their professional career and are ready 
# to bounce back into the industry. Knowing that the self-confidence and skills would need refreshing, we ensured that the 
# women in this program were put through counselling and strong technical learning sessions with a view to reinstate their 
# confidence. 
# Employee Experience 
# Candidate Experience 
# The pandemic and post-pandemic era took the ‘War for Talent’ to a new high, and attracting new talents became a 
# significant challenge. To address this, we formed the Candidate Experience team, whose focus and motto is to instill Alpha TECH Lab 
# | Alpha TECH cultural integration for the prospective candidates pre-onboarding.  
# This team works alonAlpha TECHide Talent Acquisition Group (TAG) to create a welcoming and delightful experience for candidates, 
# to increase the likelihood of joining our organization. The Candidate Experience team reaches out to candidates after TAG 
# has extended a job offer. The team provides a personalized approach to the prospects through the journey from being a 
# candidate to becoming a member of our organization. We propagate our ‘vision and mission’ and our ‘RITE values’ with 
# pride to all our candidates. Candidates are encouraged to explore our organization’s website, are shared a video tour of our 
# office, and webinar links to participate in Technical and Non-Technical sessions, provided with regular updates on events 
# and our internal monthly magazine called ‘enGAge’, to keep our candidates engaged and to learn more about our culture. 
# Additionally, the team connects candidates with their future manager and project buddy for role clarification and project-


 
 
# 7 
 
 
# related clarifications. The candidates also get to meet with the leaders virtually and at the office premises to bring about 
# the engagement. 
# Onboarding Process 
 
 
 
# Upon onboarding, the below checkpoints are ensured for a better assimilation, 
# New Joiner Orientation: Every new joiner goes through a formal induction that includes awareness around overall 
# organization culture, RITE values, vision, benefits, applicable policies & programs, and awareness with respect to business 
# and functional orientation.  


 
 
# 8 
 
 
# Role Orientation: Every person who joins a team newly has a learning curve and is given the necessary training based on the 
# role requirements. To ensure they master the curve quickly in context to requirements of the client, domain and role at the 
# earliest possible.  
# To assimilate and make a new entrants’ journey easy and swift, AMIGO (a buddy) program was introduced. Each new joiner 
# is assigned an AMIGO from the same project to support for the first 90 days. The AMIGOs are chosen based on their tenure 
# and demonstration of organizational values, culture and project awareness. The AMIGOs are provided with necessary 
# training and are expected to connect with, engage and create a sense of belonging among the new joiners.  
# SHEroes 
# At Alpha TECH Lab | Alpha TECH, women have formed a group “SHEroes” that resemble traditional networks but are exclusive. This allows 
# women to bring diversity to decision-making, establish sponsorship, and find support within the organization. Having a 
# trustworthy mentor is an essential factor in career advancement, and building deep relationships with people who support 
# you is the foundation. This community fosters trust, allowing women to speak up and share their achievements without 
# hesitation. This not only boosts confidence but also helps internalize accomplishments. To strengthen community building 
# and enhance connectivity, we have a WhatsApp group and a dedicated distribution list for all women associates across 
# business units. This enables seamless information sharing, pulse surveys, improved decision-making, getting to know each 
# other, and timely communication during emergencies 
# Business Etiquette  
# Business etiquette refers to the expected behavior and practices within a professional setting. It's essentially a set of 
# manners that ensures smooth communication, respect, and a positive work environment. 
# Communication: 
# Professionalism: Maintain a professional tone in all communication, written and verbal. Use proper grammar and avoid 
# slang or overly casual language. 
# Clarity and Conciseness: Communicate clearly and concisely, ensuring your message is understood. 
# Dress Code: 
# Business wear should always maintain a clean, neat, and professional appearance, adhering to commonly accepted 
# standards of dressing and grooming.  
# Please note that these guidelines are general and may not cover every appropriate or inappropriate item. We trust that 
# employees will use good judgment in their attire choices. It's crucial that our clothing reflects our commitment to the RITE 
# Values, Alpha TECH' Code of Conduct, and our dedication to each other and our customers. 
 


 
 
# 9 
 
 
 
# Dining Etiquette:  
# While a cafeteria setting might be more casual than a formal business lunch, there are still some basic 
# business dining etiquettes to consider at office. 
 
# Identity Cards 
# Every employee will get an ID card to enter our workplace. You'll receive your permanent ID card on your first 
# day. Use your ID card to enter and exit the building where you're allowed. Keep your card visible and show it 
# if asked.  
# An employee must immediately report loss of an ID card to the Administration Team. The Administration 
# Team will issue a duplicate card and a sum of Rs 300/- will be deducted from the employee as the cost of ID 
# card. 
# Working Days 
# Our standard workweek consists of five days, running from Monday to Friday, with Saturday and Sunday designated as 
# weekly off days. However, employees involved in projects or assignments requiring 24X7 support may be assigned to work 
# shifts and might not have Saturday and Sunday as their weekly offs. 


 
 
# 10 
 
 
# The responsibility for scheduling, communicating, and managing shift schedules lies with the Customer Success Manager or 
# Functional Head. Employees are expected to adhere to their designated working hours as per their shift. Any temporary 
# changes in working hours require approval from the respective Customer Success Manager or Functional Head. 
# Office hours 
# Our working hours are: 
# General Shift 
# 0900 hrs. to 18.00 hrs. 
# Morning shift 
# 0600 hrs. to 1500 hrs. 
# Evening shift 
# 1400 hrs. to 2200 hrs. 
# Night Shift 
# 2200 hrs. to 0600 hrs./ or as defined by the customer 
 
# Women employees working after 8:00 PM 
 
# If any women employees need to work in the office after 8:00 PM due to work requirements, safety measures will be put 
# in place for their protection when leaving the premises. 
# Time Tracking 
# We need to keep track of how many hours each employee works. This helps with thinAlpha TECH like project costs, 
# billing clients, and planning for time off. Make sure to record all your hours in the Alpha TECH system, and your 
# manager will review and approve them every week. 
# Holidays 
# We have 9 +2(optional) national or festival holidays each year. You can find the list of approved holidays on 
# the company intranet. 
# Workplace Cleanliness 
# You'll be provided with everything you need to work effectively, like a workstation and computer. Please keep 
# your workspace clean, take care of company property, and don't bring in anything unrelated to work or food. 
 
# Hardware and Software 
# If you need any hardware or software for your work, or if you have any issues with your computer or the 
# network, you can raise a ticket to the IT Support team. 
# Security 
# We want to make sure our workplace is safe, so we have security guards who may check your ID card. Please 
# cooperate with them. 


 
 
# 11 
 
 
 
# Visitors 
# If you need to meet with visitors, you can do so in the reception area or the lunchroom after registering with 
# security. 
# Visiting Cards 
# Employees in certain roles will receive visiting cards for business purposes. If you need visiting cards for your 
# job, you can request them with approval from the Business head/ Functional head. If in case you need, you 
# can raise request to admin team. 
# Network Access Agreement 
# We offer computing and communication resources, including internal network and Internet access, to 
# employees for official tasks. This access is meant to help them fulfill their job responsibilities effectively. While 
# employees can also use these resources to enhance their knowledge and productivity, it's important to 
# remember that these are company tools meant for achieving business objectives. However, we understand 
# the need for limited personal email usage, if it doesn't interfere with the company's interests. For more 
# details, refer to the Network Policy in Annexure I. 
# Proprietary Rights and Non-Disclosure Agreement 
# The Non-Disclosure and Confidentiality Agreement, outlined in Annexure II and included in your appointment 
# letter, is a vital document for all employees. It's mandatory for every employee to sign this agreement upon 
# joining the company. 
 
 
 
 
 
 
 
 
 


 
 
# 12 
 
 
 
# Part II – Your Entitlement 
 
# Alpha TECH acknowledges the significance of ensuring employees' work-life balance and actively promotes the 
# utilization of leave benefits. 
# Leave Policy: 
# Type of leave 
# Eligibility 
# Earned Leave / Annual 
# Leave 
# • 
# 20 days of leave will be credited in the beginning of the Financial year 
# (April – March) 
# • 
# At the end of year, all un-availed days will be encashed based on the 
# basic pay. 
# • 
# No leaves will be carried forward from current year to the next year 
# under any of the Leave categories.  
# Family and Emergency Leave 
# 6 days of paid leave to cater to family or in case of emergencies. This leave 
# is applicable only in the following conditions: 
# • 
# Marriage of the employee (Leave to be applied min. 2 weeks in 
# advance). 
# • 
# Death of immediate family consisting of spouse, children, siblinAlpha TECH, 
# parents, and parents in law. 
# • 
# Hospitalization of the employee or his/her immediate family consisting 
# of spouse, children, dependent parents, and parents in law. Leave shall 
# be applied in the system with proper documentation. Please note that 
# pregnancy/delivery related hospitalizations are excluded from this as 
# they are separately catered for.  
 
# Note: This leave will not be carried forward to the next financial year 
# Maternity leave 
 
# • 
# All women employees who have been with the organization for a 
# period     of 80 days in the 12 months preceding the date of delivery. 
# • 
# Maximum of 182 days of leave including all weekly offs and holidays 
# falling in between. 
# • 
# Subject to the provisions of the Maternity Benefit Act Employee availing   
# maternity leave must give adequate notice to the company for making 
# alternate arrangements. 
# • 
# Maternity leave may be availed in combination with other eligible 
# leaves     with the approval of concerned managers and HR BP. 
# • 
# In case of miscarriage, a woman employee shall avail the leave, on 
# submission of such proof as may be prescribed, be entitled to taking 
# leave with wages at the rate of maternity benefit for a period of six 
# weeks immediately following the day of her miscarriage. 
# • 
# This facility will be available for the birth of the first two children only. 


 
 
# 13 
 
 
# Paternity leave 
# • 
# Male associates will be granted 10 days of paternity leave on the birth 
# of his baby. 
# • 
# This leave can be taken in 2 splits within 6 months from the birth of 
# baby. 
# • 
# This facility will be available for the birth of the first two children only. 
# • 
# Employee should submit proof of birth to avail the paternity leave in 
# HRMS portal. 
# Sick Leave 
# • 
# 4 days of sick leave will be granted to all full-time employees.  
# • 
# 2 days will be credited for every 6 months. 
# • 
# Supporting documents to be submitted while opting this leave type. 
# Note: This leave cannot be carried forward for next financial year 
# Adoption/Surrogacy leaves 
# This policy outlines the provisions to the employees who are going to be 
# parents through adoption or surrogate birth of a child. 
# Leave Entitlements: 
# • 
# Female Employees: Upon legal adoption or surrogate birth of a child, 
# employee is eligible for 12 calendar weeks of paid Adoption/Surrogacy 
# leave, starting from the date the child is placed in their care.  
# • 
# Male Employees: Upon legal adoption of a child, male employees are 
# entitled to avail 4 calendar weeks of paid Adoption/Surrogacy leave. 
#  Sabbatical leaves 
# • 
# Unpaid leave is granted only after exhausting all other leave options. 
# • 
# All intervening holidays and weekends are count towards the leave 
# period. 
# • 
# A maximum of 90 days leave is granted with approval from CSM and HR 
# Head 
# • 
# LWP exceeding 30 days can be on medical grounds and approved by 
# CSM and HR BP 
# • 
# Employee availing Sabbatical will not be entitled for salary, 
# reimbursements, variable pay for the said period. 
# Compensatory Off 
# • 
# Employees working on a national or public holiday for 8 hours or more 
# will be eligible to take a compensatory off for the day worked. 
# • 
# Any employee, who has worked for a minimum of 8 hours on a weekly 
# off   day or on a particular day he/she has worked for an additional shift 
# of 8 hours, will be eligible for one day compensatory leave. 
# • 
# Compensatory off needs to be availed within 30 days with the prior 
# approval of the reporting manager. Compensatory off is applicable from 
# Engineer to Lead level only. 
# Note: The attendance is to be marked for 8 hours to be eligible for 
# compensatory-off 
 
 


 
 
# 14 
 
 
 
# Employee Wedding& New-born Gift 
# Alpha TECH extend best wishes to the employee and his / her spouse on the occasion of their wedding and bless and cherish the 
# arrival of the newborn along with the parents                                           
# Wedding Gift 
# In the event of an employee getting married while in the services of the organization, a gift as detailed below, will be given 
# to the employee – 
# This gift can be availed by the employee only once during his/her service with the organization 
# Payroll for Alpha TECH Entities 
# Gift Amount 
# India 
# INR 5000 
# United States of America 
# USD 100 
# Middle East 
# USD 100 
 
# New-born Gift 
# In the event of an arrival of a new-born for an employee, a gift as detailed below will be given to the employee This gift can 
# be availed by the employee only twice during his/her service with the organization. 
# Payroll for Alpha TECH Entities 
# Gift Amount 
# India 
# INR 2000 
# United States of America 
# USD 50 
# Middle East 
# USD 50 
 
# Night Shift Allowance 
 
# Eligibility - Employees at E and T levels are eligible for a night shift allowance. 
# The allowance applies if you work between 10 pm and 6 am. If you work from home, you're not eligible. Your manager or 
# shift lead will assign your shifts based on business needs. You'll get Rs. 300 per day as an allowance. The NSA will be 
# calculated based on the check-in or check-out and shift assigned in HRMS portal. 
# On-Call Allowance  
# Aims for effective resolution of urgent matters requiring attention beyond core business hours. 
# Scope & Applicability 


 
 
# 15 
 
 
# • 
# Applicable to engagements specified in SOW for billable on-call support.                 
# • 
# Covers billable hours outside regular shift roster. 
# Guidelines     
# Employees on-call must remain reachable via phone and email, with internet connectivity.  
# 2. Allowance applicable for billable support, P1 issues, and unplanned high-impact releases during non-work hours.  
# 3. Regular work hours must be completed in-office to claim allowance for weekends, holidays, or leave days.  
# 4. Compensation provided for extended on-call shifts and office visits during on-call duty.  
# 5. Excludes planned activities.  
# On-Call Allowance 
# INR 1000 or $50 per day, location dependent. 
# Additional $50 for tasks over two hours on weekends, approved by CSMs. 
# Team Lunch/Dinner Reimbursement 
 
# Purpose:  
# Fostering a positive work environment and team bonding.  
# Reimbursement Limit: Up to INR 600 per employee per claim (inclusive of taxes).  
# Frequency: Available twice in a financial year, with a 4-month gap between successive claims 
# Business Travel Policy 
 
# Coverage: Boarding, lodging, conveyance, miscellaneous, and incidental expenses during business travel.                                     
# Procedure: 
# • 
# Submission of International Travel Expenses Claim Form (Annexure 2) within 4 days of each trip. 
# • 
# Unutilized foreign exchange to be surrendered to Accounts Department within the same period. 
# • 
# Documentation of Air tickets (local and foreign), hotel bills, airport tax payment bills, food bills, and other expense 
# bills required. 
# • 
# Eligibility Calculation: Includes purchase of foreign exchange at the airport; detailed expenses breakdown required. 
 
 
 


 
 
# 16 
 
 
 
# Kit Allowance 
 
# Eligibility:  Employees up to T3 required to undertake foreign travel on company business.  
# It aimed at ensuring they are equipped with the necessary attire and accessories for their trip. This allowance, capped at 
# INR 7000, covers expenses such as suits, blazers, shoes, woollens, and luggage, essential for conducting their work 
# diligently and appropriately in the visited country. To avail this reimbursement, employees must submit relevant vouchers 
# and bills after incurring the expenses, particularly applicable to those undertaking international travel for the first time.   
 
# Provident Fund  
# The Provident Fund scheme, regulated by the Provident Fund and Miscellaneous Act, 1952, mandates a monthly 
# contribution of 12% of the basic salary from both the employee and employer. Managed by the Regional Provident Fund 
# Commissioner’s office, the accumulated funds can be transferred upon leaving the company, subject to application, and 
# can be withdrawn completely only upon discontinuation of services, with specific procedures outlined for loans, advances, 
# and withdrawals.  
 
# Insurance Coverage 
# • 
# Group Mediclaim Policy (GMC) 
# • 
# Group Personal Accident Policy (GPAP) 
# • 
# Group Term Life Insurance (GTLP) 
# Coverage Extended to  
# • 
# GMC (Employee + Spouse (if applies) + up to Two Children) 
# • 
# GMC Parents & In Laws can be covered and the employee to bear the premium for the  
# coverage 
# • 
# Top-up options are available 
# • 
# GPA (All Employees) 
# • 
# GTL (All Employees) 
# Guidelines for Group Mediclaim Policy 
# • 
# Employees can use the Cashless Claim facility for planned treatment if done in a listed network hospital.  
# • 
# Advance notification to the hospital's insurance desk is required for pre-authorization.  
# • 
# Mid-term additions to the policy are only allowed for life events like Marriage, Birth, Demise, or Divorce.  
# • 
# Exceptions require approval from the Head of HR with appropriate justifications.  
# • 
# Notification within 48 hours of admission is necessary for non-emergency hospitalizations.  
# • 
# Reimbursement claims beyond 30 days from discharge may not be processed. 
 
 


 
 
# 17 
 
 
# Sl. No. 
# Policy 
# Grade 
# Sum Insured 
# 1. 
# GMC 
# All Employees(E+S+2C) 
# INR 5,00,000 /- 
# 2. 
 
# GPAP 
# E 
# INR 15,00,000/- 
# 3. 
# T 
# INR 20,00,000/- 
# 4. 
# M, S & Executive Band 
# INR 25,00,000/- 
# 5. 
# GTL 
# All Employees 
# INR 25,00,000/- 
 
# Note 
# -  
# The Employee & parental policy provides a sum insured of INR 3,00,00/-, with additional voluntary options for top-up 
# coverage ranging from 2 Lakhs to 10 Lakhs. Employees can choose these top-up options, but they will be responsible for 
# paying the premium associated with them. 
# Transfers    
 
# During your employment with the company, the management would assign you duties and responsibilities. The company 
# might transfer you to any other unit, division or places to meet organizational exigencies and work requirements.  
# Separations 
# Alpha TECH would like to have a long-term association with each one of you and are committed to plan a long- term career for 
# each employee.  
# 1. Voluntary Separation 
# In cases where an employee opts for a voluntary resignation, he/ she shall submit the resignation through HRMS portal 
# • 
# The reporting manager along with the HRBP will initiate the retention discussion and try to sort out 
# issues with an aim to retain the employee. Upon successful retention, the employee shall revoke 
# the resignation in the HRMS 
# • 
# In case the resignation is accepted, the reporting manager and the HRBP will approve it in the HRMS 
 
# First level Approval 
# Reporting Manager 
# Final level Approval 
# HRBP (ESM) 
# 2. Involuntary Separation 
# The typical instances where the organization shall initiate a separation process: 
# All employees shall abide by the terms and conditions as mentioned in the offer letter. 
 
 


 
 
# 18 
 
 
 
# a) Unsatisfactory Performance 
# In cases of unsatisfactory performance, the concerned employee shall be apprised of his/her 
# performance and the same shall be recorded in the performance improvement plan (PIP) 
# form refer PIP process. 
 
# b) Disciplinary Action 
# In the event of an employee being found violating any organizational policies as detailed in the 
# Code of Conduct & business ethics policy and other applicable policies, investigation will 
# be carried out, if the employee is proven to be guilty, the investigation team may decide 
# appropriate action not limited only to termination. 
 
# c) Business Reasons 
# i. If need be, organization shall decide to right size the employee strength, by initiating 
# organization separation for certain employees. 
# ii. During such instances, organization shall clearly communicate the reason behind the 
# separation. Notice pay in lieu of notice period shall be paid by the organization and any 
# request by employee for early relieving shall   be   accepted and      notice pay  will be prorated 
# accordingly. 
 
# d) Negative BGV 
 
# i. When the employment gets terminated based on the negative BGV Report issued. 
 
# e) Absconding 
# ii. In case an employee absents himself/herself without any proper notice and fails to 
# communicate the same, he/she will be sent three formal communications asking to 
# report back to duty. Failing/defaulting which, the employee shall be terminated on 
# grounds of absconding. 
 
# Leave during Notice period 
 
# During the notice period, you can take leave for up to 2 days each month, depending on how much leave you have left. 
# The amount of money you'll get when leaving your job is based on what you agreed to when you first started working 
# here. But remember, if there are any changes to the company's rules about this, those changes will be followed instead of 
# what's in your agreement letter.  
 
 
 


 
 
# 19 
 
 
 
# Retirement 
# The employee will retire on completion of 60 years of age. The actual date of retirement will be the last working day of the 
# month the employee attains the retirement age.     
# Part III – Organization Growth and Employee Development 
 
# Performance Management Programme 
# Performance feedback is a continuous approach and is deemed a consistent process with a view to provide regular 
# and constructive feedback. The feedback will happen quadruple times and the following review mechanisms have 
# been created to enable employees to comprehend their progress, 
# - 
# Q1 Performance Feedback: Goals & Expectations Setting, Alignment to the overall requirement 
# - 
# Q2 Performance Feedback: Progress tracking and Feedback. Possible release of the eligible half- yearly 
# Performance Based Pay with respect to the individual performance rating and organization performance 
# - 
# Q3 Performance Feedback: Progress tracking and Feedback. 
# - 
# Q4 Performance Feedback: Annual Performance Feedback Management program. 
# Eligibility- Employees who join on or before December 31st of each year are eligible for the annual performance 
# management program. Specific eligibility criteria for quarterly performance feedback are defined and published by the 
# Organization Effectiveness team. 
#   This is a critical exercise that enables: 
# • 
# Evaluate your performance at work 
# • 
# Set new targets and Key Performance Areas 
# • 
# Evaluate training needs for improvements in the current performance and for enhanced job responsibilities. 
# Process: 
# Our Performance Management Process encompasses Goals and Behavioural Competencies. The performance outcome of 
# each full-time employee is dependent on the Performance Results (accounting for 70%) and Behavioural Competency 
# (accounting for 30%).  
# Goals 
# • 
# Balanced Score Card is followed for T4 managers and above (Annexure I) 
# • 
# Goals Tree (an extended version of the Balanced Score Card) will be followed for the delivery leaders. 
# • 
# Open goal / KRA sheets for unique roles 
# • 
# Our aspiration is to enable the entire organization with the Goals tree to have a focused growth at all 
# levels 
 
 


 
 
# 20 
 
 
 
# Behavioural Competencies 
# • 
# Defined and assigned automatically based on the level/position of the individual employee 
 
# Performance Improvement Plan Process 
# If the performance needs improvement, the reporting manager with the HR Business Partner and the employee 
# sign up the PIP process document (Refer Performance Improvement Plan Process) 
 
# The spirit of the appraisal system shall be one of mutual help through feedback rather than a criticism or judgment. The 
# employee’s development rather than evaluation would be the objective of the performance review discussion. 
# Career Path / Tracks, Grades & Designations 
 
# Career Path 
# Tracks 
# Customer Success Management 
# Digital / Consulting / Enterprise Support Services 
# Technology 
# IP / Technology/ Solutions Teams 
# Consulting 
# Business Analysis/ SAP Teams 
# Business Enablement 
# Pre-Sales / Marketing/ Alliances Teams 
# Business Support 
# Finance / Admin / HR / QMG / CSG Teams/Legal & Compliance 
# Sales 
# Sales / International Sales Teams 
 
# Annual Compensation Review 
# Your compensation package will be reviewed annually, with increments based on your performance during your tenure with 
# the organization. 
# Components of Compensation Package 
# • 
# Basic Salary & House Rent Allowance (HRA) 
# • 
# Allowances 
# • 
# Statutory Benefits 
# • 
# Variable pay based on your level 
# Details of your entitlements are outlined in your appointment letter, but please note that the structure is subject to change. 
# We expect all employees to maintain confidentiality regarding their compensation and refrain from discussing it with 
# colleagues. 
 


 
 
# 21 
 
 
 
# Rewards and Recognitions 
# Alpha TECH strongly believes that it is important to toast to the success and happiness of its employees. For the collective 
# celebrations together - the little and big joys, Alpha TECH grows to become a part of each other’s lives creating fond memories 
# with Alpha TECH etched in them. Recognition makes people feel good about themselves. It also motivates us to keep up the good 
# work. Positive reinforcement sets an example for everyone, showing them the kind of work that is valued. And it doesn’t 
# have to be an elaborate event. 
# Quarterly Awards 
# The Quarterly Awards at Alpha TECH Lab | Alpha TECH are designed to recognize and reward employees and teams for their 
# exceptional performance and contributions every quarter. These awards aim to encourage continuous excellence 
# and reinforce a culture of recognition within the organization. 
# These awards apply to all full-time employees and Retainers within Alpha TECH Lab| Alpha TECH. 
# Selection Process: 
# Each vertical, department will have the awards committee, whose responsibility is to select the most 
# qualifying individuals against the reward criteria set for the award category.   
# Star Performer of the Quarter: 
# Star award is named to acknowledge the special contribution made by an individual to create significant 
# business impact, Customer Delight, Process improvement, and exceptional contribution. 
# Star Team of the Quarter: 
# The award is extended to the best team that has demonstrated outstanding client delivery, a high level of 
# collaboration within and between teams, and achieved team goals through exemplary collective efforts with 
# minimum disruptions during the quarter. 
# Customer Delight: 
# The Customer Delight Award is granted to individuals who deliver exceptional impact, business value, and 
# superior service experiences, significantly exceeding client expectations. This recognition celebrates those 
# who elevate customer satisfaction and loyalty through outstanding performance leaving an impactful 
# experience in the mind of the customer. 
# Long Service Awards 
# Long service awards are key milestone awards for employees for their loyalty, commitment to the 
# organization vision and growth journey. These awards are on completion of 5, 10, 15, 20 & 25 year milestone 
# and would be honored with a Service plaque and reward 
 
 
 


 
 
# 22 
 
 
 
# SPOT Recognition 
# SPOT Recognition Program will recognize spontaneous contributions that are impactful and towards 
# organization initiatives, brand building and fostering a positive work culture. 
 
# The program is based on nomination by self, manager, peers, seniors, and any other stakeholder. The 
# recognition is awarded based on the nomination and approval of the contribution by respective Stakeholder 
# followed by HR Business Partner. 
 
# Training and Development  
 
# We believe that to survive in a dynamic and demanding work environment, strategic planning and quick responses to 
# training & development is the key to success. In this regard, we place a strong emphasis on Training & Development that 
# facilitates performance at the individual, team and organization level. 
# Internal TraininAlpha TECH:  
# With the availability of Subject Matter Experts, few training courses are conducted internally. The current competency is 
# evaluated through a pre-training assessment that helps in structuring the program effectively. Post training assessment is 
# conducted, and feedback is sought to capture the effectiveness of the training. 
# Additionally, project specific courses are enabled through the mechanism of Cohort syncs which ensures seamless 
# integration of assigning appropriate courses to the respective colleague. The Learning Management System also acts as our 
# Learning Repository wherein all internal traininAlpha TECH are converted as courses along with specific assessments and is available 
# to all for their self-learning journey. 
 
# External TraininAlpha TECH:  
# Our Learning Academy has a strong industry affiliation and partnership with reputable learning partners who are leaders in 
# their technology & process areas. This includes strategic industry academia partnerships with IIT Madras on various channels 
# of capability building. These include focus on Healthcare, BFS and the Hi-Tech verticals.  
# Domain Institutes:  
# 1. Alpha TECH Lab | Alpha TECH Institute of Healthcare AI Technology (GIHT) -   
# The objective of this program is to help participants:   
# • 
# Understand the various stakeholders involved in Healthcare in India and globally, and their roles in patient care   
# • 
# Grasp key processes in healthcare operations across stakeholder organizations   
# • 
# Understand the role and impact of IT in supporting the various stakeholder operations   


 
 
# 23 
 
 
# Additionally, the Healthcare Warrior program with IIT-Madras is enabled which is a tailor-made AI/ML intensive designed to 
# provide technologists with the in-depth knowledge and skills they need to understand, develop and apply AI methods in 
# healthcare and life science. 
 
# 2. Alpha TECH Lab | Alpha TECH Institute of Financial Technology (GIFT) -   
# By the end of the course, students will be able to:  
# • 
# Have a strong understanding of the foundations of Banking & Financial sector   
# • 
# Understand the different regulations governing the domain   
# • 
# Understand the role of IT operations in enabling banks to offer better and reliable services to their customers   
# • 
# Gain insights into the leading trends and technologies in the financial space  
 
# Academia Collaboration:  
# We have various strategic industry academia partnerships with IIT Madras, Chime University & NPTEL (National Programme 
# on Technology Enhanced Learning - A Joint Learning Initiative by the IITs & IISC) on various channels of capability building.  
# We have recently collaborated with the IIT and IISc hosted Industry Accelerator Program for a series of virtual webinars on 
# the Healthcare domain. These events bring together students, healthcare professionals, IT specialists, researchers, and 
# academic faculty who are passionate about leveraging technology to improve patient care. 
 
# Certification Reimbursements:  
# Employees can opt for certification based on their interests that will fuel their growth at Alpha TECH Lab | Alpha TECH. Based on the prior 
# approvals from the Reporting Manager & Customer Success Managers (CSMs) these certifications and exclusive training will 
# be reimbursed thereby catering to both individual and organizational goals. 
 
# Career Development Plan (CDP): 
# Growth and development are an important facet of an employee’s journey. Each colleague's growth trajectory is unique and 
# requires customized plans and support. As an organization with a firm belief in building a High-Performance culture, there 
# is an unrelenting need to support the employees in bringing their ‘A game’. This gets addressed by three major aspects – a 
# clear goal alignment derived from the business goals and strategy, a nurturing and effective performance feedback 
# conversation, and an intensive plan to develop oneself.  
# Effective Performance Feedback is provided through our quarterly appraisals for continuous improvement. All employees 
# are assigned with a Career Development Plan (CDP) as an outcome of Performance Management Program (PMP), focusing 
# on short term & long-term development needs. The manager and employee jointly define the CDP based on the current & 
# future scope and capability requirements. 
 


 
 
# 24 
 
 
 
# Part IV– POSH (Prevention of Sexual Harassment) 
 
#  -     RAKSHA Committee 
# *An eight-member committee, including an external Ombudsperson- Ms. Reshmi Christy, is responsible for investigating 
# and addressing reports of sexual harassment. Employees who experience or witness harassment are encouraged to report 
# it immediately to the Functional Head/HR Head or email raksha@Alpha TECHtech.com. The function of the committee is to receive, 
# objectively investigate the reported incident and take it to a logical conclusion. * 
#  -      Reporting Process 
# Employees should provide details of the incident, including time, venue, and individuals involved. The RAKSHA Committee 
# will conduct a thorough investigation, maintaining confidentiality and treating all parties with respect and compassion.  
# - 
# Disciplinary Procedure 
# It is crucial for understanding the standards of behaviour expected within the company and the process for addressing any 
# misconduct. It applies to all employees, emphasizing fairness and consistency. The procedure begins with informal 
# resolution, where managers address minor issues directly. If the matter persists or is serious, a formal investigation is 
# conducted before any disciplinary action is taken. Employees are informed in writing of any allegations against them and 
# given an opportunity to respond. Throughout the process, employees have the right to be accompanied by a colleague or 
# representative. The company also values equality and diversity, ensuring fair treatment for all. Confidentiality is maintained 
# throughout the procedure, and efforts are made to adhere to set timescales. Different approaches are taken for minor and 
# serious misconduct, with disciplinary sanctions ranging from warninAlpha TECH to dismissal based on the severity of the offense. 
# Overall, the procedure aims to maintain a professional work environment while ensuring that employees are treated fairly 
# and consistently. 
 
 
 
# At Alpha TECH, we are committed to fostering a work environment that is free from 
# harassment and conducive to professional growth. Sexual harassment is strictly 
# prohibited, and any employee found guilty of such behaviour will face disciplinary 
# action, including possible suspension or termination.     


 
 
# 25 
 
 
 
# Part V – Our Expectations from You 
 
# Your Commitment 
# As an employee of Alpha TECH, you are expected to honour certain commitments towards the organization. Commitment towards 
# achieving business objectives 
# • 
# Continuous enhancement of skills and ability 
# • 
# Abide by organizational norms 
# • 
# To uphold and foster organizational values 
# • 
# To abide by the confidentiality agreement 
# • 
# To function effectively as a team 
# Note: This book contains only general information about the current policies and procedures. Policies and procedures are 
# subject to change and at the discretion of the management. 
# Annexure-I   Network Security and Usage Policy 
# Introduction 
# Alpha TECH provides computing and communication facilities, including internal network and Internet access (Network facilities), 
# to employees solely for their work in the Company, in order to complete responsibilities assigned to them. In addition, 
# judicious use of these facilities is permitted to enable the employees to become better informed and more productive at 
# work. Employees are expected to be aware, at all times that the Network facilities are the Company’s business tolls and are 
# to be used solely for the purpose of achieving the company’s business goals and objectives. However, the Company 
# understands the need for sending/receiving personal text mail to a reasonable extent, not conflicting with the Company’s 
# business interests. 
# The facilities and nature of access provided would be dependent on an employee’s level and responsibilities. Employees 
# with access to Network facilities must take particular care to understand the copyright, trademark, libel, slander and public 
# speech control laws of all countries in which the Company maintains a business presence, so that use of the Network facilities 
# does not inadvertently violate any laws, which may be enforceable against the Company. 
# The Network facilities are susceptible to misuse; it should be the endeavour of every employee to safeguard these facilities 
# against such misuse, wilful or otherwise. It is only through such total and sustained discipline on the part of every employee 
# that the Company reaps the benefits of the Network facilities without compromising its security. The overriding principle is 
# that Security of the Network is to be everyone’s first concern. 


 
 
# 26 
 
 
# The Company Network Security and Usage Policy are based on this principle. The specific policy provisions are listed below. 
# The Corporate Services Group (CSG) will implement and interpret this policy and their decision will be final. 
# Definition 
# Alpha TECH communication facilities include but are not limited to: 
# • 
# Any email system 
# • 
# Any software used by Alpha TECH that can communicate or interface with other software 
# • 
# The Alpha TECH home page 
# • 
# Access to other internal and external systems, database and gateways, portals, extranets and intranets. 
# • 
# Networked and standalone access to public Intranet and the World Wide Web. 
# Appropriate Use/Security 
# The workstation hardware, software, test tools, test equipment etc., network resources like server access, Internet mail, 
# Web, FTP and other accesses are to be used by every person only for the official work being performed by them in the 
# Company. However, employees may use Network facilities for research or browsing in relation to their technical learning 
# outside the regular working hours. They should not use the facility for personal gains, including posting of resumes, soliciting 
# job offers or furthering personal business interests Employees should not use the Company’s facilities to download and 
# install or distribute any software or data. Specific materials, documents, manuals for the purpose of work can, however, be 
# downloaded by employees. Any such files or software may be used only in ways that are consistent with their licenses or 
# copyrights. 
# Employees should use only software provided by CSG or any customer, since use of non-authorized software represents a 
# serious threat to the security of the network. 
# The Company has the right to inspect all files stored in any workstation’s server or any area of the Company’s network. The 
# Company will conduct routine audit of all hardware and software installed in every system and any files or data other than 
# those provided by CSG or internally developed by the person or the team for the work currently being performed will be 
# treated as unauthorized storage. 
# The Company has installed a variety of security systems, including firewalls, proxies and Internet address screening 
# programs, to protect the security of the network. Employees should not attempt to circumvent or disable or overload the 
# network or any system intended to protect the privacy or security of the computers or the network, except when required 
# in the course of their official duties. Any attempt to do so will be treated as misconduct. 
# To maintain the security of the network systems provided by the company employees should not 


 
 
# 27 
 
 
# Disclose the password or lend the authentication details or allow access to anyone not employed by Alpha TECH, where a password 
# or authentication device controls access to the system. 
# Disclose their login password (or any authentication device) to their immediate business colleagues within the company for 
# business operational purposes only. In all circumstances and situations, employees must keep such password secure. 
# Attempt unauthorized access to or use of any system, network or information owned by the company or its client or any 
# other party. 
# Attempt to probe the security of any system or network or engage in any type of computer hacking activity unless you are 
# expressly authorized by the company to actively engage in security development or testing of a particular system or product. 
# Without being expressly authorized by the company, deliberately attempt to obtain access or assist another person to 
# deliberately attempt to obtain access to secured accounts, email, documents or other files, including using software tools 
# to obtain password or keys or to effect decryption or access information in the files of another staff member. 
# Employee shouldn’t knowingly propagate any virus, worm, Trojan, Horse or trap door program code. In the event of any 
# employee coming to know of such code in his or her computer, it should be informed to the CSG immediately. 
# Employees should not use Network facilities to store or propagate materials that is: 
# • 
# Sexually explicit or inappropriate 
# • 
# Derogatory or offensive 
# • 
# Racist 
# • 
# Disparaging of the Company, its employee, associates, customers, clients, policies or procedures. 
# • 
# Jokes, stories, chain letters and similar material. 
# • 
# For amusement or for playing games.  
# Confidentiality 
# The Company reserves the right to block access to any website including those providing the above. In case any of the 
# employees inadvertently visit such sites, he or she should immediately disconnect from that site and should inform the CSG. 
# Employees should not use or store or transmit to anyone else, in any manner, any software, data, proposals, design 
# documents, technical specifications, customer requirements, unless it is required for the performance of their work. 
# Employee should not transmit Company information of any kind, including Company Confidential, financial, marketing 
# material, human resource information to anyone else, unless authorized to do so. 
# Employees should especially be conscious of Intellectual Property when using any software, data, proposals, design 
# documents, technical specifications, customer requirements, documents or manuals, whether provided by the Company or 


 
 
# 28 
 
 
# by any of its associates, customers or clients. Such material should be used only for the specific purpose and specific project 
# activity for which it has been given to them. 
# Sharing or software, data or files between machines on the network should be done with care and adequate 
# protections/precautions and should be done only for specific purpose and without violating any confidentiality or 
# intellectual property of the Company or its customers, vendors, prospects and associates. The Company reserves the right 
# to monitor and record all Network traffic, including email, chat or newsgroup messages. No employee should have any 
# expectation of privacy as to his or her Network usage. The CSG will record all the activity and analyze usage patterns and 
# may publicize this data if necessary. 
# The Company reserves the right to block or filter Network traffic based on criteria such as size, subject matter, source or 
# destination etc. 
# The Company Network facilities should not be used knowingly to violate the laws of the Republic of India or any other nation 
# or of any state or local body. Use of the Company resources for any illegal activity would be treated as misconduct. The 
# Company will comply with reasonable requests from law enforcement and regulatory agencies for loAlpha TECH, diaries or archives 
# on an individual’s Network activities or usage of Network facilities. 
# Any employee using the Network facilities is required to identify oneself honestly, completely and accurately when 
# participating in chats or newsgroups or when setting up internally authorized accounts on outside computer systems. 
# The Company retains the copyright to any material posted to any forum, newspaper group, chat or World Wide Web page 
# by any employee. 
# Misconduct 
# Using the Company’s Network facilities to commit infractions such as misuse of the Company’s assets or resources, sexual 
# harassment and misappropriation or theft of intellectual property are also prohibited; any such infraction would be treated 
# as a misconduct. 
# Annexure II - Proprietary Rights and Non-Disclosure Agreement 
# Terms and Conditions of Employment 
# In consideration of the employment of the undersigned (“Employee”) by Alpha TECH Technologies Private Ltd. (the “Company”), and as 
# a condition of continued employment, Employee agrees as follows: 
# Ownership and Non -Disclosure of Proprietary Information 
# The employee acknowledges that all Proprietary Information, as defined below, is the exclusive property of the Company or the party 
# that disclosed or delivered the same to the Company. Specifically, Employee agrees that all Proprietary Information developed as a 


 
 
# 29 
 
 
# direct or indirect result of the Employee’s efforts during any period of employment with the Company shall be and shall remain the 
# exclusive property of the Company, and the Employee shall have no ownership interest therein. To the extent Employee may have 
# any interest in such developed Proprietary Information, Employee assigns such interest to the Company. While employed by the 
# Company for three (3) years thereafter, the Employee shall not use or disclose any Proprietary  
# Information, directly or indirectly, except as authorized by the Company in connection with Employee’s assigned duties. The 
# foregoing notwithstanding, Employee shall not in any time use or disclose, directly or indirectly, any of the Proprietary Information 
# Constituting Trade Secrets of the Company, as defined below, except as authorized by the Company in connection with Employee’s 
# assigned duties. 
# Definitions 
# Propriety Information, as referred to herein, includes all of the following information and material, whether or not reduced to 
# writing and whether or not patentable, the Employee during any period of employment with the Company has access to or 
# develops in whole or in part as a direct or indirect result of such employment or through the use of any of the Company’s 
# facilities or resources:  
# (i) Application, operating system, communication and other computer software, including without limitation all source and object 
# code, flow charts, algorithms, coding sheets, routines, sub-routines, compilers, assemblers, design concepts and related 
# documentation and manuals;  
# (ii)Production processes, marketing techniques, purchasing information, fee lists, licensing policies, quoting procedures, 
# financial information, employee names and job descriptions, customer and prospective customer names and requirements, 
# data and other information or material relating to the way any customer, prospective customer of the Company do business;  
# (iii)Discoveries, concepts and ideas (including but not limited to the nature and results of research and development 
# activities), processes, formulae, techniques, “know-how”, designs, drawinAlpha TECH and specifications;  
# (iv)Any other information or material relating to business or activities of the Company which is not generally known to others 
# engaged in similar business or activities;  
# (v)All inventions and ideas which are derived from or relate to Employee’s access to or knowledge of any of the information 
# or material described herein; and  
# (vi) Any information of raw materials described herein which is the property of any other person or firm which has revealed 
# or delivered such information or material to the Company pursuant to a contractual relationship with the Company or 
# otherwise the sources of the Company’s business. 
# “Proprietary Information” shall not include any information or material of the type described herein to the extent that such 


 
 
# 30 
 
 
# information or material is or becomes publicly known through no act on Employee’s part. “Trade Secrets”, as preferred 
# herein, include all of the information and material described in paragraphs (i), (ii), (iii), (iv), (v) and (vi). The failure to mark 
# any of the Proprietary Information as confidential shall not affect its status as Proprietary Information or Trade Secrets. 
# Records 
# All notes, data, reference material, sketches, drawinAlpha TECH, memoranda, and records in any way relating to any 
# of the Proprietary Information or the Company’s business shall belong exclusively to the Company, and at 
# request of the Company or, in the absence of such a request, upon the termination of the Employee’s 
# employment with the Company, Employee agrees to turn over to the Company all such materials and copies 
# thereof in Employee’s possession 
# Injunctive Relief 
# Because of the valuable and unique nature of Proprietary Information, Employee understands and agrees 
# that the Company shall suffer irreparable harm if the Employee breaches any of the Employee’s obligation 
# under this Agreement and that monetary damages shall be inadequate to compensate the Company for any 
# breach thereof. Accordingly, Employee agrees that, in addition to any other remedies or rights, the Company 
# shall have the rights to obtain an injunction to force the terms of this agreement 
# Previous Employer 
# Employee represents that the Employee’s performance as an employee of the Company will not breach any 
# employment agreement nor any agreement to keep in confidence any trade secret, confidential or propriety 
# information of a former employer. Employee has not brought any trade secrets, confidential or propriety 
# information of a former employer to the company. Employees will not disclose nor use in the performance of 
# Employee’s work with the Company any trade secrets, confidential or authorization from the former 
# employer. 
# Non-Solicitation 
# Until two (2) years after the termination of employment with the Company, Employee will not solicit or otherwise encourage 
# others to leave the Company’s employment 
 
 
 
 
 


 
 
# 31 
 
 
 
# Annexure – III - Declaration form by women Employees Leaving Office Premises after 
# 8p.m. 
# Employee ID 
# : 
# Employee Name 
# : 
# Address 
# : 
# Contact Number 
# : 
# Date / Out Time / Time Reached Home 
# : 
# / 
# / 
# Mode of Transport 
# : 
# Company 
# provided 
# cab 
# (Yes / No) If no, then Public Transport / Bike / Car 
# Department / Project 
# : 
# SU / Function 
# : 
# Manager Name 
# : 
# Accompanying Employee ID 
 
# :  
# Accompanying Employee Name 
# :  
# Accompanying Employee Contact Number:  
# Emergency Contact Number 
 
# :  
# State the reason for leaving the premises after 8pm: 
 
# Declaration of taking own Transportation: 
 
# I understand that Alpha TECH insists all female employees working after 8 pm to take the transport provided by 
# office in which I am avoiding taking up the service due to my own transport arrangement and that it is my 
# sole responsibility for doing so. I also hereby Declare that I shall hold blameless indemnify Alpha TECH, their 
# employees, officers and agents from any loss, cost, damages and / or Expense any nature which I may have 
# resulted, either directly or indirectly in taking my own transportation arrangement by avoiding company 
# facility. 
# Employee signature 
# Security Signature 
# Date: 


 
 
# 32 
 
 
# Annexure IV – Business Travel 
# Annexure 1: Allowance Chart – Local Conveyance, Domestic& Overseas Travel 
# Domestic Travel 
# All employees required to proceed on outstation duties within India shall be entitled to the following: 
 
# Level 
# Mode of 
# Travel 
# Class 
# of 
# Travel 
# Lodging 
# Boarding 
# Local 
# Conveyance 
# E to S 
# Air 
# Economy 
# Company 
# arranged 
# As 
# per 
# bills 
# Actuals 
 
# If the distance to be traveled is less than 5hrs or 250kms then the travel by air is restricted and a suitable 
# alternate mode of transport must be taken. 
# Employees travelling to the outstation by Road, in their own car, for official purposes, will be reimbursed at 
# the rate of Rs.15/- per kilometer. 
# Travel on Business Visa 
# A) The following are the entitlements for travel on Business Visa. 
 
# Location 
# Level Mode 
# and 
# Class of 
# Travel 
 
 
 
# Lodging 
# Per diem 
# Local 
# Travel 
# Laundry 
# Telephone 
# USA 
# Middle 
# East 
# Singapore, & 
# all 
# other 
# countries 
# other than UK 
# S 
# Air (Business Class) 
# Actuals 
# Actuals 
# & USD 25 per 
# week 
# for 
# Miscellaneous 
# expenses. 
# Taxi 
# Actuals 
# Actuals 
 
# T 
# Air (Economy) 
# Actuals 
# USD 50 
# Taxi 
# Actuals 
# Actuals 
 
 
# M 
# Air (Economy) 
# Actuals 
# USD 50 
# Taxi 
# Actuals 
# Actuals 


 
 
# 33 
 
 
 
# E 
# Air (Economy) 
# Actuals 
# USD 50 
# Taxi 
# Actuals 
# Actuals 
 
 
 
 
 
 
 
 
# UK 
# S 
# Air (Business Class) 
# Actuals 
# Actuals 
# Taxi 
# Actuals 
# Actuals 
 
# E, M 
# &T 
# Air (Economy) 
# Actuals 
# UK 
# 45 
# Pounds 
# Taxi 
# Actuals 
# Actuals 
 
# Non- Billable employees will be reimbursed expenses on actuals and no per diem is payable. However, they will be eligible 
# for an out-of-pocket expense of USD 25 per week, (20 Pounds per week, if the travel is to UK). Fraction of a week is to be 
# treated as a week. No supporting’s or  bills are required for this claim. 
# Annexure V – Expenses Claim Form
                               
#                                """}])  # Wrap the string properly



def encode_audio(data: np.ndarray) -> str:
    """Encode Audio data to send to the server"""
    return base64.b64encode(data.tobytes()).decode("UTF-8")


class GeminiHandler(AsyncStreamHandler):
    """Handler for the Gemini API"""

    def __init__(
        self,
        expected_layout: Literal["mono"] = "mono",
        output_sample_rate: int = 24000,
    ) -> None:
        super().__init__(
            expected_layout,
            output_sample_rate,
            input_sample_rate=16000,
        )
        self.input_queue: asyncio.Queue = asyncio.Queue()
        self.output_queue: asyncio.Queue = asyncio.Queue()
        self.quit: asyncio.Event = asyncio.Event()

    def copy(self) -> "GeminiHandler":
        return GeminiHandler(
            expected_layout="mono",
            output_sample_rate=self.output_sample_rate,
        )

    async def start_up(self):
        if not self.phone_mode:
            await self.wait_for_args()
            api_key, voice_name = self.latest_args[1:]
        else:
            api_key, voice_name = None, "Puck"

        client = genai.Client(
            api_key=api_key or os.getenv("GEMINI_API_KEY"),
            http_options={"api_version": "v1alpha"},
        )

        config = LiveConnectConfig(
            response_modalities=["AUDIO"],  # type: ignore
            system_instruction=sys_instruct,
            speech_config=SpeechConfig(
                voice_config=VoiceConfig(
                    prebuilt_voice_config=PrebuiltVoiceConfig(
                        voice_name=voice_name,
                    )
                )
            ),
        )
        async with client.aio.live.connect(
            model="gemini-2.0-flash-exp", config=config
        ) as session:
            async for audio in session.start_stream(
                stream=self.stream(), mime_type="audio/pcm"
            ):
                if audio.data:
                    array = np.frombuffer(audio.data, dtype=np.int16)
                    self.output_queue.put_nowait((self.output_sample_rate, array))

    async def stream(self) -> AsyncGenerator[bytes, None]:
        while not self.quit.is_set():
            try:
                audio = await asyncio.wait_for(self.input_queue.get(), 0.1)
                yield audio
            except (asyncio.TimeoutError, TimeoutError):
                pass

    async def receive(self, frame: tuple[int, np.ndarray]) -> None:
        _, array = frame
        array = array.squeeze()
        audio_message = encode_audio(array)
        self.input_queue.put_nowait(audio_message)

    async def emit(self) -> tuple[int, np.ndarray] | None:
        return await wait_for_item(self.output_queue)

    def shutdown(self) -> None:
        self.quit.set()


stream = Stream(
    modality="audio",
    mode="send-receive",
    handler=GeminiHandler(),
    rtc_configuration=rtc_configuration,
    concurrency_limit=5 if get_space() else None,
    time_limit=90 if get_space() else None,
    additional_inputs=[
        gr.Textbox(
            label="API Key",
            type="password",
            value=os.getenv("GEMINI_API_KEY") if not get_space() else "",
        ),
        gr.Dropdown(
            label="Voice",
            choices=[
                "Puck",
                "Charon",
                "Kore",
                "Fenrir",
                "Aoede",
            ],
            value="Puck",
        ),
    ],
)


class InputData(BaseModel):
    webrtc_id: str
    voice_name: str
    api_key: str


app = FastAPI()

stream.mount(app)


@app.post("/input_hook")
async def _(body: InputData):
    stream.set_input(body.webrtc_id, body.api_key, body.voice_name)
    return {"status": "ok"}


@app.get("/")
async def index():
    rtc_config = await get_cloudflare_turn_credentials_async() if get_space() else None
    html_content = (current_dir / "index.html").read_text()
    html_content = html_content.replace("__RTC_CONFIGURATION__", json.dumps(rtc_config))
    return HTMLResponse(content=html_content)


if __name__ == "__main__":
    import os

    if (mode := os.getenv("MODE")) == "UI":
        stream.ui.launch(server_port=7860)
    elif mode == "PHONE":
        stream.fastphone(host="0.0.0.0", port=7860)
    else:
        import uvicorn

        uvicorn.run(app, host="0.0.0.0", port=7860)

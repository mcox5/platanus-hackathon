
'''
        {
            "question_id": {
                "score": assigned_score,
                "feedback": "a brief comment explaining the assigned score"
            }
        }
        
        {
            "2": { 
                "score": 5, 
                "feedback": "The student's answer is incomplete as it misses a valid argument." 
            }
        }

'''

tool_list = [
    {
        "name": "evaluate_student_answer",
        "description": "Evaluate how accurate the student's answer is based on a guideline and the answer provided as context.",
        "inputSchema": {
            "json": {
                "type": "object",
                "properties": {
                    "question_id": {
                        "type": "string",
                        "description": "Indicates the id of the question to evaluate."
                    },
                    "score": {
                        "type": "integer",
                        "description": "Evaluate the accuracy of the student's answer on a scale from 1-10",
                        "minimum": 1,
                        "maximum": 10
                    },
                    "feedback": {
                        "type": "string",
                        "description": "A brief comment explaining the assigned score"
                    }
                },
                "required": [
                    "question_id", 
                    "score", 
                    "feedback"
                ]
            }
        }
    }
]

example_tool_list = [
    {
        "toolSpec": {
            "name": "summarize_email",
            "description": "Summarize email content.",
            "inputSchema": {
                "json": {
                    "type": "object",
                    "properties": {
                        "summary": {
                            "type": "string",
                            "description": "A brief one-line or two-line summary of the email."
                        },
                        "escalate_complaint": {
                            "type": "boolean",
                            "description": "Indicates if this email is serious enough to be immediately escalated for further review."
                        },
                        "level_of_concern": {
                            "type": "integer",
                            "description": "Rate the level of concern for the above content on a scale from 1-10",
                            "minimum": 1,
                            "maximum": 10
                        },
                        "overall_sentiment": {
                            "type": "string",
                            "description": "The sender's overall sentiment.",
                            "enum": ["Positive", "Neutral", "Negative"]
                        },
                        "supporting_business_unit": {
                            "type": "string",
                            "description": "The internal business unit that this email should be routed to.",
                            "enum": ["Sales", "Operations", "Customer Service", "Fund Management"]
                        },
                        "customer_names": {
                            "type": "array",
                            "description": "An array of customer names mentioned in the email.",
                            "items": { "type": "string" }
                        },
                        "sentiment_towards_employees": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "employee_name": {
                                        "type": "string",
                                        "description": "The employee's name."
                                    },
                                    "sentiment": {
                                        "type": "string",
                                        "description": "The sender's sentiment towards the employee.",
                                        "enum": ["Positive", "Neutral", "Negative"]
                                    }
                                }
                            }
                        }
                    },
                    "required": [
                        "summary",
                        "escalate_complaint",
                        "overall_sentiment",
                        "supporting_business_unit",
                        "level_of_concern",
                        "customer_names",
                        "sentiment_towards_employees"
                    ]
                }
            }
        }
    }
]

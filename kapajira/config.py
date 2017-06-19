"""
JIRA access config
"""
JIRA_CONFIG = {
    "url":      '',
    "user":     '',
    "password": '',
    #List of Jira project names - kapajira looks for a component defined in each of them matching the service name
    #and files the ticket in it. If no match is found, first project on the list is used.
    "projects":  []
}

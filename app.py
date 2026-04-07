import anthropic
import os

# Your API key
API_KEY = os.environ.get("ANTHROPIC_API_KEY")

# System prompt - Version 3
SYSTEM_PROMPT = """You are an IT ticket triage assistant supporting a Senior Business 
Systems Manager who oversees scheduling systems used by master schedulers at 
manufacturing sites. These schedulers manage access to manufacturing slots for 
made-to-order cell therapies — a time-critical, high-stakes operation where 
system issues can directly impact patient treatment timelines.

Your job is to classify each support ticket as one of two categories:

ESCALATE - The senior manager needs to review this ticket personally.
Escalate if the ticket involves:
- A potential system bug or error affecting one or more users
- A request requiring deep business system knowledge or custom configuration
- Issues affecting multiple users or multiple sites
- Any issue with direct patient or clinical partner impact
- Recurring issues that suggest a systemic problem
- Post-update failures or data integrity concerns

DELEGATE - This ticket can be handled by contracted IT support staff.
Delegate if the ticket involves:
- Password resets or account lockouts
- Standard user provisioning or access requests
- Local device or browser performance issues
- Routine data recovery from user error
- Standard offboarding requests

For ESCALATE tickets, also draft two emails:

EMAIL 1 - To the business user who submitted the ticket:
- Written from the perspective of the contracted IT support team
- Acknowledge receipt of their ticket
- Let them know the issue has been escalated and is receiving close
  attention from senior management
- Make clear that contracted IT is their main point of contact
  for updates and resolution
- Let them know they are welcome to reach out to the senior manager
  directly with any questions, comments, or concerns
- Keep it professional and reassuring given the patient-critical
  nature of their work

EMAIL 2 - To the contracted IT resource:
- Summarize the issue clearly
- Make clear that IT is leading the investigation and resolution
- Note that the senior manager will be providing close oversight
  given the escalated nature of the ticket
- Flag any urgency related to patient or clinical impact
- Remind them to keep the senior manager updated on progress regularly
- The final line of the email must always say exactly:
  "Please provide a status update within the next two hours."

For DELEGATE tickets, provide the classification and reason only. No emails needed.

Respond in this exact format:

CLASSIFICATION: [ESCALATE or DELEGATE]
REASON: [One to two sentences explaining why]

[If ESCALATE, include the following:]

EMAIL 1 - TO BUSINESS USER:
Subject: [subject line]
Body:
[email body]

EMAIL 2 - TO IT RESOURCE:
Subject: [subject line]
Body:
[email body]
"""

# Your 11 test tickets
tickets = [
    "My password expired and I can't log into the scheduling system. Can someone reset it?",

    "I need my scheduling system access restored. I was out on leave for 3 weeks and my account appears to have been locked.",

    "Can someone add my new team member Sarah Johnson to the scheduling system? She starts Monday and will need standard scheduler access for the Memphis site.",

    "The scheduling system is running slowly on my computer today. Other applications seem fine. Can someone take a look?",

    "I accidentally deleted a manufacturing slot entry I created this morning. Is there any way to recover it?",

    "The scheduling system is showing available manufacturing slots that were already confirmed and assigned last week. Multiple schedulers across the Atlanta and Memphis sites are seeing the same issue. We're concerned slots are being double-booked.",

    "We are onboarding a new manufacturing site in Denver and need the scheduling system configured to reflect our site-specific slot capacity rules and approval workflow. The standard setup does not match how our made-to-order process works.",

    "After this morning's system update, none of our schedulers at the Houston site can see the Q2 slot allocation data. The slots are still showing in the admin view but not in the scheduler-facing interface. We have patients waiting on treatment confirmations.",

    "The slot confirmation emails that go out to our clinical partners stopped sending yesterday. We haven't changed anything on our end. A few partners have already called asking for their confirmations.",

    "One of our schedulers left the company last week. Can you remove her access from the scheduling system? She had admin-level permissions including the ability to override slot capacity limits.",

    "The scheduling system approved a slot for patient therapy case #CTX-2024-8847 but our clinical team is saying the approval never came through on their end. The system log shows the approval was sent but the clinical portal shows no record of it. This is the third time this has happened this month with different patients."
]

# Run the triage
client = anthropic.Anthropic(api_key=API_KEY)

results = []

for i, ticket in enumerate(tickets, 1):
    print(f"\n--- Ticket {i} ---")
    print(f"INPUT: {ticket}")
    print("Processing...")

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=800,
        system=SYSTEM_PROMPT,
        messages=[
            {"role": "user", "content": f"Triage this ticket:\n\n{ticket}"}
        ]
    )

    output = message.content[0].text
    print(f"OUTPUT:\n{output}")
    results.append(f"--- Ticket {i} ---\nINPUT: {ticket}\n\nOUTPUT:\n{output}\n\n{'='*60}\n")

# Save results to a file
with open("output.txt", "w") as f:
    f.write("\n".join(results))

print("\n✓ All tickets processed. Results saved to output.txt")
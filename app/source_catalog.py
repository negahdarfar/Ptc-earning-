"""Curated first-party discovery queue. These are leads, not eligibility claims."""
from sqlmodel import Session, select

from .models import SourceLead


# All entries are deliberately seeded as unreviewed research leads. Provider
# eligibility, payout rails, fees, and terms must be checked for the operator.
INITIAL_SOURCE_LEADS = (
    {
        "platform_key": "upwork", "platform_name": "Upwork",
        "category": "client_services", "source_url": "https://www.upwork.com/",
        "source_type": "client_services",
        "review_notes": "Research lead only. Start with manual workflow; API access requires separate provider approval.",
    },
    {
        "platform_key": "fiverr", "platform_name": "Fiverr",
        "category": "client_services", "source_url": "https://www.fiverr.com/",
        "source_type": "client_services",
        "review_notes": "Research lead only. Verify current seller terms, payout methods and country rules.",
    },
    {
        "platform_key": "gumroad", "platform_name": "Gumroad",
        "category": "digital_product", "source_url": "https://gumroad.com/",
        "source_type": "digital_product",
        "review_notes": "Research lead only. Verify creator onboarding and country-specific payout coverage.",
    },
    {
        "platform_key": "amazon-associates", "platform_name": "Amazon Associates",
        "category": "affiliate", "source_url": "https://affiliate-program.amazon.com/",
        "source_type": "affiliate",
        "review_notes": "Research lead only. Verify the relevant local program, traffic rules and payout requirements.",
    },
    {
        "platform_key": "clickworker", "platform_name": "Clickworker",
        "category": "microtask", "source_url": "https://www.clickworker.com/",
        "source_type": "microtask",
        "review_notes": "Research lead only. Registration, task supply and payout options vary by country.",
    },
    {
        "platform_key": "prolific", "platform_name": "Prolific",
        "category": "research", "source_url": "https://www.prolific.com/",
        "source_type": "research",
        "review_notes": "Research lead only. Participation is limited to supported countries and account verification.",
    },
    {
        "platform_key": "contra", "platform_name": "Contra",
        "category": "client_services", "source_url": "https://contra.com/",
        "source_type": "client_services",
        "review_notes": "Research lead only. Verify independent-contractor eligibility, fees, payout rails and country coverage.",
    },
    {
        "platform_key": "freelancer", "platform_name": "Freelancer.com",
        "category": "client_services", "source_url": "https://www.freelancer.com/",
        "source_type": "client_services",
        "review_notes": "Research lead only. Verify project fees, withdrawal minimums, identity checks and country coverage.",
    },
    {
        "platform_key": "peopleperhour", "platform_name": "PeoplePerHour",
        "category": "client_services", "source_url": "https://www.peopleperhour.com/",
        "source_type": "client_services",
        "review_notes": "Research lead only. Verify seller onboarding, service fees and supported withdrawal methods.",
    },
    {
        "platform_key": "toptal", "platform_name": "Toptal",
        "category": "client_services", "source_url": "https://www.toptal.com/",
        "source_type": "client_services",
        "review_notes": "Research lead only. Selection is competitive; verify screening, contract terms and payment eligibility.",
    },
    {
        "platform_key": "99designs", "platform_name": "99designs",
        "category": "client_services", "source_url": "https://99designs.com/",
        "source_type": "client_services",
        "review_notes": "Research lead only. Verify designer fees, contest terms, payout methods and regional availability.",
    },
    {
        "platform_key": "etsy", "platform_name": "Etsy",
        "category": "digital_product", "source_url": "https://www.etsy.com/",
        "source_type": "digital_product",
        "review_notes": "Research lead only. Verify Etsy Payments country eligibility, listing fees and digital-item policies.",
    },
    {
        "platform_key": "ko-fi", "platform_name": "Ko-fi",
        "category": "digital_product", "source_url": "https://ko-fi.com/",
        "source_type": "digital_product",
        "review_notes": "Research lead only. Verify payment-processor support, platform fees and content rules.",
    },
    {
        "platform_key": "patreon", "platform_name": "Patreon",
        "category": "digital_product", "source_url": "https://www.patreon.com/",
        "source_type": "digital_product",
        "review_notes": "Research lead only. Verify creator eligibility, platform fees, payout methods and tax requirements.",
    },
    {
        "platform_key": "envato", "platform_name": "Envato",
        "category": "digital_product", "source_url": "https://market.envato.com/",
        "source_type": "digital_product",
        "review_notes": "Research lead only. Verify author applications, item review, revenue share and payout terms.",
    },
    {
        "platform_key": "creative-market", "platform_name": "Creative Market",
        "category": "digital_product", "source_url": "https://creativemarket.com/",
        "source_type": "digital_product",
        "review_notes": "Research lead only. Verify shop approval, product licensing, fees and payout availability.",
    },
    {
        "platform_key": "adobe-stock", "platform_name": "Adobe Stock Contributor",
        "category": "digital_product", "source_url": "https://contributor.stock.adobe.com/",
        "source_type": "digital_product",
        "review_notes": "Research lead only. Verify contributor eligibility, content licensing, tax forms and payout thresholds.",
    },
    {
        "platform_key": "shutterstock", "platform_name": "Shutterstock Contributor",
        "category": "digital_product", "source_url": "https://submit.shutterstock.com/",
        "source_type": "digital_product",
        "review_notes": "Research lead only. Verify contributor terms, content rights, tax details and payout methods.",
    },
    {
        "platform_key": "freepik-contributor", "platform_name": "Freepik Contributor",
        "category": "digital_product", "source_url": "https://contributor.freepik.com/",
        "source_type": "digital_product",
        "review_notes": "Research lead only. Verify contributor acceptance, licensing, revenue share and payout rules.",
    },
    {
        "platform_key": "impact", "platform_name": "impact.com",
        "category": "affiliate", "source_url": "https://impact.com/",
        "source_type": "affiliate",
        "review_notes": "Research lead only. Verify advertiser approval, promotion rules, thresholds and payment coverage.",
    },
    {
        "platform_key": "partnerstack", "platform_name": "PartnerStack",
        "category": "affiliate", "source_url": "https://partnerstack.com/",
        "source_type": "affiliate",
        "review_notes": "Research lead only. Verify partner acceptance, program-specific terms, commissions and withdrawal options.",
    },
    {
        "platform_key": "awin", "platform_name": "Awin",
        "category": "affiliate", "source_url": "https://www.awin.com/",
        "source_type": "affiliate",
        "review_notes": "Research lead only. Verify publisher approval, advertiser rules, payment thresholds and country support.",
    },
    {
        "platform_key": "cj-affiliate", "platform_name": "CJ Affiliate",
        "category": "affiliate", "source_url": "https://www.cj.com/",
        "source_type": "affiliate",
        "review_notes": "Research lead only. Verify publisher onboarding, advertiser-specific rules and payout eligibility.",
    },
    {
        "platform_key": "rakuten-advertising", "platform_name": "Rakuten Advertising",
        "category": "affiliate", "source_url": "https://rakutenadvertising.com/",
        "source_type": "affiliate",
        "review_notes": "Research lead only. Verify publisher approval, market availability, commission terms and payment details.",
    },
    {
        "platform_key": "usertesting", "platform_name": "UserTesting",
        "category": "research", "source_url": "https://www.usertesting.com/get-paid-to-test",
        "source_type": "research",
        "review_notes": "Research lead only. Human participation only; verify applicant eligibility and supported payout method.",
    },
    {
        "platform_key": "user-interviews", "platform_name": "User Interviews",
        "category": "research", "source_url": "https://www.userinterviews.com/",
        "source_type": "research",
        "review_notes": "Research lead only. Verify participant location, study screening, incentive delivery and availability.",
    },
    {
        "platform_key": "respondent", "platform_name": "Respondent",
        "category": "research", "source_url": "https://www.respondent.io/",
        "source_type": "research",
        "review_notes": "Research lead only. Human research participation only; verify location, screening and incentive terms.",
    },
    {
        "platform_key": "telus-digital-ai", "platform_name": "TELUS Digital AI Community",
        "category": "microtask", "source_url": "https://www.telusdigital.com/careers/ai-community",
        "source_type": "microtask",
        "review_notes": "Research lead only. Verify project-specific country, language, assessment and payment requirements.",
    },
    {
        "platform_key": "oneforma", "platform_name": "OneForma",
        "category": "microtask", "source_url": "https://www.oneforma.com/",
        "source_type": "microtask",
        "review_notes": "Research lead only. Verify project availability, qualification rules, country and payout options.",
    },
    {
        "platform_key": "outlier", "platform_name": "Outlier",
        "category": "microtask", "source_url": "https://outlier.ai/",
        "source_type": "microtask",
        "review_notes": "Research lead only. Verify expert/project eligibility, country coverage, task supply and payout terms.",
    },
)


def seed_initial_source_leads(session: Session) -> int:
    """Insert missing curated leads without overwriting operator review decisions."""
    inserted = 0
    for item in INITIAL_SOURCE_LEADS:
        existing = session.exec(
            select(SourceLead).where(SourceLead.platform_key == item["platform_key"])
        ).first()
        if existing:
            continue
        session.add(SourceLead(**item))
        inserted += 1
    if inserted:
        session.commit()
    return inserted

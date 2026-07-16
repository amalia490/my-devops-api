import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def trimite_email_breaking_news(emailuri_destinatari, sursa_nume, titlu_stire, link_stire):
    if not emailuri_destinatari:
        return 
    
    SENDER_EMAIL = "-----"
    SENDER_PASSWORD = "-----"

    subiect = f" BREAKING NEWS: {sursa_nume}"
    
    corp_mesaj = f"""
    Salut,
    
    A apărut o nouă știre importantă pe {sursa_nume}:
    
    🔴 {titlu_stire}
    
    Citește tot articolul aici: {link_stire}
    
    O zi excelentă,
    Echipa NewsRadar
    """

    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['Subject'] = subiect
    msg.attach(MIMEText(corp_mesaj, 'plain'))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls() 
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            
            for email in emailuri_destinatari:
                msg['To'] = email
                server.send_message(msg)
                print(f"Email trimis cu succes catre: {email}")
                
    except Exception as e:
        print(f" Eroare la trimiterea emailului: {e}")
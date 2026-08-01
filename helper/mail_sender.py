import os
import resend

sender_email = os.getenv("EMAIL")
resend.api_key = os.getenv("RESEND_API_KEY")

    
def send_mail(user_email, otp):
    print(sender_email)
    try:
        params: resend.Emails.SendParams = {
        "from": sender_email,
        "to": [user_email],
        "subject": "Your OTP!",
        "html": f"""<strong> Your OTP is : {otp}</strong></br><p>Copy this code to verify your account</p>""",
        }
        email = resend.Emails.send(params)
        return {"success":True, "message":email}
    except Exception as err:
        import traceback
        traceback.print_exc()
        return {"success":False, "message":str(err)}
    
# send_mail()
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.exceptions import PermissionDenied
from rest_framework import status

from django.http import HttpResponse
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django_otp import user_has_device
from django_otp.plugins.otp_totp.models import TOTPDevice
from django.utils import timezone
from io import BytesIO
import base64
import qrcode
import qrcode.image.svg
# Create your views here.

class LoginView(APIView):
    permission_classes = (AllowAny,)
    def post(self,request):
        if request.user.is_anonymous:
            try:
                user=User.objects.get(username=request.data["username"])
            except ObjectDoesNotExist:
                raise PermissionDenied({"detail":"Nome utente e/o password non validi"})
            if user.check_password(request.data["password"]):



                if user_has_device(user): #se ha il device creato e confermato
                    try:
                        device=TOTPDevice.objects.get(user=user,confirmed=True)
                        isAllowed=device.verify_is_allowed()
                        if "otp_token" in request.data:
                            if not isAllowed[0]:
                                delta=isAllowed[1]["locked_until"]-timezone.now()
                                raise PermissionDenied({"detail":"Attendi "+str(int(delta.total_seconds()))+" secondi prima di inviare il nuovo OTP"})                    
                            if device.verify_token(request.data['otp_token']):
                                for token in Token.objects.filter(user=user):
                                    token.delete()
                                token=Token(user=user)
                                token.save()
                                return Response({"token":token.key})
                        else:
                            return Response({"detail":"Inserisci OTP"})
                        raise PermissionDenied("OTP non valido")
                    except KeyError:
                        raise PermissionDenied("OTP non valido")
                else:
                    if "otp_token" in request.data:
                        # se il device esiste:
                        if TOTPDevice.objects.filter(user=user,confirmed=False).exists():
                            #confermalo
                            device=TOTPDevice.objects.get(user=user,confirmed=False)
                            isAllowed=device.verify_is_allowed()
                            if not isAllowed[0]:
                                delta=isAllowed[1]["locked_until"]-timezone.now()
                                raise PermissionDenied({"detail":"Attendi "+str(int(delta.total_seconds()))+" secondi prima di inviare il nuovo OTP"})                    
                            if device.verify_token(request.data['otp_token']):
                                device.confirmed=True
                                device.save()
                                for token in Token.objects.filter(user=user):
                                    token.delete()
                                token=Token(user=user)
                                token.save()
                                return Response({"token":token.key})
                            else:
                                raise PermissionDenied({"detail":"OTP non valido"})                    
                        #se il device non esiste:
                        raise PermissionDenied("Non permesso")
                    else:
                        for totp in TOTPDevice.objects.filter(user=user,confirmed=False):
                            totp.delete()
                        
                        device=TOTPDevice(user=user,name="AMOS - "+user.username,confirmed=False,tolerance=0)
                        device.save()
                        ## BUG otpauth://totp/
                        config_url=device.config_url[:15]+"AMOS - "+device.config_url[15:]
                        
                        img = qrcode.make(config_url, image_factory=qrcode.image.svg.SvgImage)
                        buffer = BytesIO()
                        img.save(buffer)
                        qr_str = base64.b64encode(buffer.getvalue()).decode()
                        return Response({"qrcode":qr_str})
            
            raise PermissionDenied({"detail":"Nome utente e/o password non validi"})
        return Response({"detail":"Sei già loggato"})
        
            
        
class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request):
        Token.objects.get(user=request.user).delete()
        return Response({"detail":"Logout eseguito!"})



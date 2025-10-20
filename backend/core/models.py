from django.db import models

class Patient(models.Model):
    SECTORS = (("trauma","Traumatología"), ("hemo","Hemodinamia"))
    ESTADOS = (
        ("Pendiente","Pendiente"),
        ("Solicitado","Solicitado"),
        ("Rechazado por cobertura","Rechazado por cobertura"),
        ("Autorizado","Autorizado"),
        ("Autorizado material pendiente","Autorizado material pendiente"),
    )
    nombre = models.CharField(max_length=180)
    dni = models.CharField(max_length=32, blank=True, default="")
    email = models.EmailField(blank=True, default="")
    telefono = models.CharField(max_length=80, blank=True, default="")
    cobertura = models.CharField(max_length=160, blank=True, default="")
    medico = models.CharField(max_length=160, blank=True, default="")
    observaciones = models.TextField(blank=True, default="")
    fecha_cx = models.DateField(null=True, blank=True)
    sector_code = models.CharField(max_length=16, choices=SECTORS, default="trauma")
    estado = models.CharField(max_length=64, choices=ESTADOS, default="Pendiente")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} ({self.dni})"

def upload_to(instance, filename):
    return f"patients/{instance.patient_id}/{filename}"

class Attachment(models.Model):
    KINDS = (
        ("orden","Orden"),
        ("dni","DNI"),
        ("credencial","Credencial"),
        ("materiales","Materiales"),
        ("otro","Otro"),
    )
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="attachments")
    kind = models.CharField(max_length=32, choices=KINDS, default="otro")
    file = models.FileField(upload_to=upload_to)
    name = models.CharField(max_length=160, blank=True, default="")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.kind} - {self.patient_id}"

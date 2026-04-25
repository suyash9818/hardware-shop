# Lookup models for fastener attribute system
# These tables store the valid values for each attribute type

from django.db import models


class LookupFamily(models.Model):
    """Fastener family: BOLT, SCR, SET, STUD, ROD-THRD, NUT, etc."""
    code = models.CharField(max_length=16, unique=True)  # BOLT, SCR, SET, STUD, etc.
    name = models.CharField(max_length=64)  # Bolt, Screw, Set Screw, etc.
    ref_no = models.PositiveIntegerField(default=100)

    class Meta:
        ordering = ["ref_no"]

    def __str__(self):
        return f"{self.code} - {self.name}"


class LookupThread(models.Model):
    """Thread size: M1.6x0.35, M2x0.40, M3x0.50, etc."""
    code = models.CharField(max_length=16, unique=True)  # M1.6x0.35, M2x0.40, etc.
    applies_to_family = models.ManyToManyField(
        LookupFamily, 
        related_name="thread_types",
        blank=True
    )
    ref_no = models.PositiveIntegerField(default=100)

    class Meta:
        ordering = ["ref_no"]

    def __str__(self):
        return self.code


class LookupHead(models.Model):
    """Head type: Hex Head, Hex Flange, Socket Head, Button Head, etc."""
    code = models.CharField(max_length=16, unique=True)  # HX, HX-FLANGE, SH, BH, etc.
    description = models.CharField(max_length=128)  # Hex Head, Socket Head Cap, etc.
    applies_to_family = models.ManyToManyField(
        LookupFamily,
        related_name="head_types",
        blank=True
    )
    ref_no = models.PositiveIntegerField(default=100)

    class Meta:
        ordering = ["ref_no"]

    def __str__(self):
        return f"{self.code} - {self.description}"


class LookupDrive(models.Model):
    """Drive type: Hex Socket, Phillips, Pozidriv, Torx, etc."""
    code = models.CharField(max_length=16, unique=True)  # HEXINT, PH, POZI, TORX, etc.
    description = models.CharField(max_length=128)  # Hex Socket (Allen), Phillips, etc.
    applies_to_family = models.ManyToManyField(
        LookupFamily,
        related_name="drive_types",
        blank=True
    )
    ref_no = models.PositiveIntegerField(default=100)

    class Meta:
        ordering = ["ref_no"]

    def __str__(self):
        return f"{self.code} - {self.description}"


class LookupMaterial(models.Model):
    """Material: Stainless Steel 304, 316, A2-70, Steel 8.8, etc."""
    code = models.CharField(max_length=16, unique=True)  # SS304, SS316, A2-70, STEEL-8.8, etc.
    description = models.CharField(max_length=128)  # Stainless Steel 304, etc.
    applies_to_family = models.ManyToManyField(
        LookupFamily,
        related_name="material_types",
        blank=True
    )
    ref_no = models.PositiveIntegerField(default=100)

    class Meta:
        ordering = ["ref_no"]

    def __str__(self):
        return f"{self.code} - {self.description}"


class LookupFeature(models.Model):
    """Feature: Nylon Insert Lock, Prevailing Torque, Keps, etc."""
    code = models.CharField(max_length=16, unique=True)  # NYLOCK, PREV-TORQUE, KEPS, etc.
    description = models.CharField(max_length=128)  # Nylon Insert Lock, etc.
    ref_no = models.PositiveIntegerField(default=100)

    class Meta:
        ordering = ["ref_no"]

    def __str__(self):
        return f"{self.code} - {self.description}"


class LookupFinish(models.Model):
    """Finish: Zinc Plated, Hot Dip Galvanized, etc."""
    code = models.CharField(max_length=16, unique=True)  # ZINC, ZINC-BLUE, GALV-HDG, etc.
    description = models.CharField(max_length=128)  # Zinc Plated, Zinc Plated (Blue), etc.
    ref_no = models.PositiveIntegerField(default=100)

    class Meta:
        ordering = ["ref_no"]

    def __str__(self):
        return f"{self.code} - {self.description}"
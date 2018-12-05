from django.db import models


class D001Object(models.Model):

    obj_id = models.IntegerField(unique=True)

    def __unicode__(self):
        return unicode(self.obj_id)


class D001BLC(models.Model):

    d001_object = models.ForeignKey(D001Object, related_name="blcs")
    ksBinHJD = models.DecimalField(max_digits=13, decimal_places=8, null=True)
    ksBinMag = models.DecimalField(max_digits=5, decimal_places=3, null=True)
    ksBinMagErr = models.DecimalField(
        max_digits=4, decimal_places=3, null=True
    )

    def __unicode__(self):
        return u"{}: {},{},{}".format(
            self.d001_object, self.ksBinHJD, self.ksBinMag, self.ksBinMagErr
        )


class D001LC(models.Model):

    d001_object = models.ForeignKey(D001Object, related_name="lcs")
    filter = models.IntegerField(null=True)
    HJD = models.DecimalField(max_digits=13, decimal_places=8, null=True)
    MJD = models.DecimalField(max_digits=13, decimal_places=8, null=True)
    pawNum = models.IntegerField(null=True)
    ZPErr = models.DecimalField(max_digits=4, decimal_places=3, null=True)

    ap1Mag = models.DecimalField(max_digits=5, decimal_places=3, null=True)
    ap1MagErr = models.DecimalField(max_digits=4, decimal_places=3, null=True)

    ap2Mag = models.DecimalField(max_digits=5, decimal_places=3, null=True)
    ap2MagErr = models.DecimalField(max_digits=4, decimal_places=3, null=True)

    ap3Mag = models.DecimalField(max_digits=5, decimal_places=3, null=True)
    ap3MagErr = models.DecimalField(max_digits=4, decimal_places=3, null=True)

    ap4Mag = models.DecimalField(max_digits=5, decimal_places=3, null=True)
    ap4MagErr = models.DecimalField(max_digits=4, decimal_places=3, null=True)

    ap5Mag = models.DecimalField(max_digits=5, decimal_places=3, null=True)
    ap5MagErr = models.DecimalField(max_digits=4, decimal_places=3, null=True)

    nChip = models.IntegerField(null=True)
    PSFClass = models.IntegerField(null=True)
    ell = models.DecimalField(max_digits=3, decimal_places=2, null=True)
    angSep = models.DecimalField(max_digits=4, decimal_places=3, null=True)

    def __unicode__(self):
        return unicode(self.d001_object)


class D001PLC(models.Model):

    d001_object = models.ForeignKey(D001Object, related_name="plcs")
    ksHJD = models.DecimalField(max_digits=13, decimal_places=8, null=True)
    ksPawNum = models.IntegerField(null=True)
    chip = models.IntegerField(null=True)
    ksMag = models.DecimalField(max_digits=5, decimal_places=3, null=True)
    ksMagErr = models.DecimalField(max_digits=4, decimal_places=3, null=True)

    def __unicode__(self):
        return unicode(self.d001_object)


class D001Var(models.Model):

    d001_object = models.ForeignKey(D001Object, related_name="vars")
    ksBestAper = models.IntegerField(null=True)
    ksMinMag = models.DecimalField(max_digits=5, decimal_places=3, null=True)
    ksMaxMag = models.DecimalField(max_digits=5, decimal_places=3, null=True)
    ksTotAmp = models.DecimalField(max_digits=4, decimal_places=3, null=True)
    ksMeanMag = models.DecimalField(max_digits=6, decimal_places=4, null=True)
    ksSdevMag = models.DecimalField(max_digits=5, decimal_places=4, null=True)
    ksWmeanMag = models.DecimalField(max_digits=6, decimal_places=4, null=True)
    ksWsdevMag = models.DecimalField(max_digits=5, decimal_places=4, null=True)
    ksMedianMag = models.DecimalField(
        max_digits=6, decimal_places=4, null=True
    )
    ksMADMag = models.DecimalField(max_digits=5, decimal_places=4, null=True)
    ksMWMSSD = models.DecimalField(max_digits=6, decimal_places=4, null=True)
    ksSigRat = models.DecimalField(max_digits=4, decimal_places=2, null=True)
    nKsSucDiff = models.IntegerField(null=True)
    nKsPaw = models.IntegerField(null=True)
    nKsEp = models.IntegerField(null=True)
    ksSkew = models.DecimalField(max_digits=5, decimal_places=3, null=True)
    ksKurt = models.DecimalField(max_digits=5, decimal_places=3, null=True)
    nKsOmit = models.IntegerField(null=True)
    critKsSigRat = models.DecimalField(
        max_digits=4, decimal_places=2, null=True
    )
    ratCritKsSigRat = models.DecimalField(
        max_digits=4, decimal_places=2, null=True
    )
    ksStet = models.DecimalField(max_digits=5, decimal_places=3, null=True)
    nKsStet = models.IntegerField(null=True)
    ksStetKurt = models.DecimalField(max_digits=4, decimal_places=3, null=True)
    ksStetMod = models.DecimalField(max_digits=5, decimal_places=3, null=True)
    ksCritStet = models.DecimalField(max_digits=4, decimal_places=3, null=True)
    ratKsCritStet = models.DecimalField(
        max_digits=5, decimal_places=3, null=True
    )
    hWmeanMag = models.DecimalField(max_digits=6, decimal_places=3, null=True)
    hWsdevMag = models.DecimalField(max_digits=6, decimal_places=3, null=True)
    nHPaw = models.IntegerField(null=True)
    hHJD = models.DecimalField(max_digits=11, decimal_places=6, null=True)
    jWmeanMag = models.DecimalField(max_digits=6, decimal_places=3, null=True)
    jWsdevMag = models.DecimalField(max_digits=6, decimal_places=3, null=True)
    nJPaw = models.IntegerField(null=True)
    jHJD = models.DecimalField(max_digits=11, decimal_places=6, null=True)
    yWmeanMag = models.DecimalField(max_digits=6, decimal_places=3, null=True)
    yWsdevMag = models.DecimalField(max_digits=6, decimal_places=3, null=True)
    nYPaw = models.IntegerField(null=True)
    yHJD = models.DecimalField(max_digits=11, decimal_places=6, null=True)
    zWmeanMag = models.DecimalField(max_digits=6, decimal_places=3, null=True)
    zWsdevMag = models.DecimalField(max_digits=6, decimal_places=3, null=True)
    nZPaw = models.IntegerField(null=True)
    zHJD = models.DecimalField(max_digits=11, decimal_places=6, null=True)
    RA = models.DecimalField(max_digits=10, decimal_places=7, null=True)
    DEC = models.DecimalField(max_digits=10, decimal_places=7, null=True)
    GLSFreq = models.DecimalField(max_digits=7, decimal_places=6, null=True)
    GLSPow = models.DecimalField(max_digits=4, decimal_places=3, null=True)
    maxFreq = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    nFreq = models.IntegerField(null=True)
    GLSFAP = models.DecimalField(max_digits=9, decimal_places=8, null=True)
    freqRes = models.DecimalField(max_digits=7, decimal_places=6, null=True)
    PDMTheta = models.DecimalField(max_digits=7, decimal_places=6, null=True)
    PDMFREQ = models.DecimalField(max_digits=7, decimal_places=6, null=True)
    PDMFAP = models.DecimalField(max_digits=7, decimal_places=6, null=True)

    def __unicode__(self):
        return unicode(self.d001_object)

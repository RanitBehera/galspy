from galspec.IO.Attribute import _Attr

class _RSGAttribute:
    def __init__(self, path: str) -> None:
        self.path = path

        with open(self.path) as f:
            self.contents=f.read()

        lines=self.contents.split("\n")[:-1]

        self.BoxSize                    = _Attr(lines[0])
        self.box_size                   = self.BoxSize()

        self.CMBTemperature             = _Attr(lines[1])
        self.cmb_temperature            = self.CMBTemperature()

        self.HubbleParam                = _Attr(lines[2])
        self.hubble_param               = self.HubbleParam()

        self.MassTable                  = _Attr(lines[3])
        self.mass_table                 = self.MassTable()

        self.Omega0                     = _Attr(lines[4])
        self.omega0                     = self.Omega0()

        self.OmegaBaryon                = _Attr(lines[5])
        self.omega_baryon               = self.OmegaBaryon()

        self.OmegaLambda                = _Attr(lines[6])
        self.omega_lambda               = self.OmegaLambda()

        self.RSDFactor                  = _Attr(lines[7])
        self.rsd_factor                 = self.RSDFactor()

        self.Time                       = _Attr(lines[8])
        self.time                       = self.Time()  

        self.UsePeculiarVelocity        = _Attr(lines[9])
        self.use_peculiar_velocity      = self.UsePeculiarVelocity()

        # self.BoxSizeUnit    = "Kilo-parsec"          #<---get thse from paramgadegt file
        # self.CMBTemperatureUnit="Kelvin"

    def __str__(self) -> str:
        return self.contents

    def __repr__(self) -> str:
        return self.contents
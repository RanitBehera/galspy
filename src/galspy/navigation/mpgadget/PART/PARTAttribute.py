from galspec.IO.Attribute import _Attr

class _PARTAttribute:
    def __init__(self, path: str) -> None:
        self.path = path

        with open(self.path) as f:
            self.contents=f.read()

        lines=self.contents.split("\n")[:-1]

        self.BoxSize                    = _Attr(lines[0])
        self.box_size                   = self.BoxSize()

        self.CMBTemperature             = _Attr(lines[1])
        self.cmb_temperature            = self.CMBTemperature()

        self.DensityKernel              = _Attr(lines[4])
        self.density_kernel             = self.DensityKernel()

        self.HubbleParam                = _Attr(lines[5])
        self.hubble_param               = self.HubbleParam()

        self.MassTable                  = _Attr(lines[6])
        self.mass_table                 = self.MassTable()

        self.Omega0                     = _Attr(lines[7])
        self.omega0                     = self.Omega0()

        self.OmegaBaryon                = _Attr(lines[8])
        self.omega_baryon               = self.OmegaBaryon()

        self.OmegaLambda                = _Attr(lines[9])
        self.omega_lambda               = self.OmegaLambda()

        self.RSDFactor                  = _Attr(lines[10])
        self.rsd_factor                 = self.RSDFactor()

        self.Time                       = _Attr(lines[11])
        self.time                       = self.Time()  

        self.TimeIC                     = _Attr(lines[12])
        self.time_ic                    = self.TimeIC()

        self.TotNumPart                 = _Attr(lines[13])
        self.tot_num_part               = self.TotNumPart()

        self.TotNumPartInit             = _Attr(lines[14])
        self.tot_num_part_init          = self.TotNumPartInit()

        self.UnitLength_in_cm           = _Attr(lines[15])
        self.unit_length_un_cm          = self.UnitLength_in_cm()

        self.UnitMass_in_g              = _Attr(lines[16])
        self.unit_mass_in_g             = self.UnitMass_in_g()

        self.UnitVelocity_in_cm_per_s   = _Attr(lines[17])
        self.unit_velocity_in_cm_per_s  = self.UnitVelocity_in_cm_per_s()

        self.UsePeculiarVelocity        = _Attr(lines[18])
        self.use_peculiar_velocity      = self.UsePeculiarVelocity()

        # self.BoxSizeUnit    = "Kilo-parsec"          #<---get thse from paramgadegt file
        # self.CMBTemperatureUnit="Kelvin"

    def __str__(self) -> str:
        return self.contents

    def __repr__(self) -> str:
        return self.contents
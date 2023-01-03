"""Physical constants."""

import functools

CACHE_MAXSIZE = int(1e6)

# CODATA 2018
# https://doi.org/10.1103/RevModPhys.93.025010
# http://physics.nist.gov/constants
c = 299792458.0
h = 6.62607015e-34
hbar = 1.054571817e-34
Ry = 10973731.568160
Ry_c = 3.2898419602508e15
e = 1.602176634e-19
m_e = 9.1093837015e-31
alpha = 7.2973525693e-3
En_h = alpha ** 2.0 * m_e * c ** 2.0
a0 = hbar / (m_e * c * alpha)
mu_B = e * hbar / (2.0 * m_e)
gamma_e = 0.5772156649015329

# positronium mass
mass = 2.0 * m_e
# reduced electron mass/ m_e
mu_me = 0.5
# Rydberg constant for positronium
Ry_ps = Ry * mu_me
# Bohr radius for Ps
a_ps = a0 / mu_me

# atomic unit scaling data :: dict(keys=(dimension, units))
conversion_data = dict()

# energy
conversion_data["energy"] = dict()
conversion_data["energy"]["SI"] = conversion_data["energy"]["joule"] = conversion_data[
    "energy"
]["J"] = En_h
conversion_data["energy"]["electronvolt"] = conversion_data["energy"]["eV"] = En_h / e
conversion_data["energy"]["Hz"] = En_h / h
conversion_data["energy"]["/m"] = En_h / (c * h)
conversion_data["energy"]["/cm"] = conversion_data["energy"][
    "wavenumbers"
] = conversion_data["energy"]["kayser"] = (conversion_data["energy"]["/m"] / 100.0)

# length
conversion_data["length"] = dict()
conversion_data["length"]["SI"] = conversion_data["length"]["meter"] = conversion_data[
    "length"
]["m"] = a0
conversion_data["length"]["cm"] = conversion_data["length"]["m"] * 100.0

# electric field
conversion_data["electric field"] = dict()
conversion_data["electric field"]["SI"] = conversion_data["electric field"][
    "V/m"
] = En_h / (e * a0)
conversion_data["electric field"]["V/cm"] = (
    conversion_data["electric field"]["V/m"] * 100.0
)


def atomic_units(dimension, nargs=1):
    """Convert the units of functions that return atomic units.

    Parameters
    ----------
    dimension : str
        Name of the unit type, e.g., 'energy' or 'length'
    nargs=1 : int
        Number of returned items to convert

    Examples
    --------
    >>> @atomic_units('energy')
    >>> def func(value, **kwargs):
    >>>    return value

    >>> func(1.0, units='eV')
    27.211386470176983
    """
    data = conversion_data[dimension]

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, units=None, **kwargs):
            if units is None or units in ["au", "atomic_units"]:
                # no conversion
                return func(*args, **kwargs)
            elif units in data:
                # convert au
                result = func(*args, **kwargs)
                if isinstance(result, tuple):
                    return tuple(
                        data[units] * r if i < nargs else r
                        for i, r in enumerate(result)
                    )
                else:
                    return data[units] * result
            else:
                supported_units = list(data.keys())
                raise ValueError(
                    f"unrecognised {dimension} units : {units} \n"
                    + f"supported units: {supported_units}"
                )

        return wrapper

    return decorator


def convert_au(value, dimension, units):
    """Convert 'value' from atomic units.

    Parameters
    ----------
    value : Number or numpy.ndarray()
    dimension : str
        e.g., 'energy' or 'length'
    units : str
        e.g., 'joule' or 'SI'

    Returns
    -------
    float
    """
    return atomic_units(dimension)(lambda: value)(units=units)


def revert_au(value, dimension, units):
    """Revert 'value' to atomic units.

    Parameters
    ----------
    value : Number or numpy.ndarray()
    dimension : str
        e.g., 'energy' or 'length'
    units : str
        e.g., 'joule' or 'SI'

    Returns
    -------
    float
    """
    return value / atomic_units(dimension)(lambda: 1)(units=units)

import numpy, argparse, pandas, scipy
from helpers import helpers

# argument setup

parser = argparse.ArgumentParser()
parser.add_argument("--input_file", type=str, help="parquet file generated by variable_creation.py")
parser.add_argument("--output_file", type=str, help="name of output file, with path.")
parser.add_argument('--level', type=float, help="the level to interpolate to.")
parser.add_argument("--variable", type=str, help="variable to compute")
parser.add_argument("--pressure_buffer", type=float, nargs='?', const=100.0, default=100.0, help="pressure range to keep on either side of the pressure ROI")
parser.add_argument("--pressure_index_buffer", type=int, nargs='?', const=5, default=5, help="minimum number of elements to preserve in the pressure buffer margins")
args = parser.parse_args()

# load data
df = pandas.read_parquet(args.input_file, engine='pyarrow')

# interpolate everything to specified level
df[[args.variable+'_interpolation', 'flag']] = df.apply(
    lambda row: pandas.Series(helpers.interpolate_to_levels(row, args.variable, [args.level])),
    axis=1
)
# dump any rows that failed to interpolate
df = df[~df[args.variable].apply(lambda x: numpy.isnan(x[0]) )].reset_index(drop=True)

df.to_parquet(args.output_file, engine='pyarrow')

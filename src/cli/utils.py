import pandas as pd
import numpy as np
from typing import Tuple

def generate_foreign_key(df, target_col, drop_target_col=True, index_name='idx'):
  df= df.copy()
  df[target_col] = df[target_col].str.lower().replace({
      'unknown': 'others', np.nan: 'others', None: 'others'
      })
  unique_vals = df[target_col].unique()

  lookup = pd.DataFrame({
      target_col: unique_vals
  }).reset_index(names=index_name)

  df = df.join(lookup.set_index(target_col), on=target_col, rsuffix=target_col)
  if drop_target_col:
    df.drop(columns=target_col, inplace=True)
  return lookup, df

def generate_many_many(df, target_col, delimeter=';', drop_target=True) -> Tuple[pd.DataFrame, pd.DataFrame]:
  df = df.copy()
  splitted = df[target_col].str.split(delimeter, expand=True).reset_index(names=['hf_id'])

  relationship_df = splitted.melt(
    id_vars='hf_id',
    value_name = target_col
  ).dropna()
  relationship_df = relationship_df[['hf_id', target_col]].reset_index(drop=True)

  lookup = pd.DataFrame({
  target_col : relationship_df[target_col].unique()
  }).reset_index(names=f"{target_col}_id")
  relationship_df = relationship_df.join(lookup.set_index(target_col), on=target_col, rsuffix=target_col)

  return lookup, relationship_df, df.drop(columns=[target_col])

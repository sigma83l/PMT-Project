import pandas as pd

def ema_crossover_strategy(df, fast_period=9, slow_period=21):
    """
    Adds EMA crossover buy/sell signals to the DataFrame.
    
    Parameters:
    - df: DataFrame with at least a 'close' column.
    - fast_period: int, shorter EMA period.
    - slow_period: int, longer EMA period.

    Returns:
    - DataFrame with added 'EMA_Fast', 'EMA_Slow', and 'signal' columns.
    """

    df = df.copy()
    df['EMA_Fast'] = df['close'].ewm(span=fast_period, adjust=False).mean()
    df['EMA_Slow'] = df['close'].ewm(span=slow_period, adjust=False).mean()

    df['signal'] = 0
    df.loc[df['EMA_Fast'] > df['EMA_Slow'], 'signal'] = 1
    df.loc[df['EMA_Fast'] < df['EMA_Slow'], 'signal'] = -1

    return df
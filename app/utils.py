def preprocess_data_for_pipeline(df):
    try:
        df['mileage'] = df['mileage'].apply(
            lambda x: float(x.split()[0])
        )
        if df['mileage'].isnull().all():
            raise ValueError("All values in 'mileage' are invalid or missing.")

        df['engine'] = df['engine'].apply(
            lambda x: float(x.split()[0])
        )
        if df['engine'].isnull().all():
            raise ValueError("All values in 'engine' are invalid or missing.")

        df['max_power'] = df['max_power'].apply(
            lambda x: float(x.split()[0]))
        if df['max_power'].isnull().all():
            raise ValueError("All values in 'max_power' are invalid or missing.")

        if 'torque' in df.columns:
            df.drop(columns=['torque'], inplace=True)

        if 'seats' in df.columns:
            df['seats'] = df['seats'].astype('object')

    except Exception as e:
        raise ValueError(f"Error during preprocessing: {str(e)}")

    return df
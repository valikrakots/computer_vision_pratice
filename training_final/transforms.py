import albumentations as A


first = A.Compose(
    [
        A.OneOf(
            [
                A.Blur(p=1.0),
                A.Sharpen(p=1.0)
            ]
        )
    ]
)

second = A.Compose(
    [
        A.ColorJitter(always_apply=True)
    ]
)
from hscode.models import Heading


p, created = Heading.objects.get_or_create(
    first_name='John',
    last_name='Lennon',
    defaults={'birthday': date(1940, 10, 9)},
)
for _, row in hs.iterrow():
    if len(row['HS']) == 4:
        _, heading = Heading.objects.get_or_create(
            no=row['HS']
        )
        product.heading = heading
        product.save()
        heading.save()

    else:
        _, subheading = SubHeading.objects.get_or_create(
            no=row['HS']
        )
        product.subheading = subheading
        product.save()
        subheading.save()

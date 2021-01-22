from profile_generator.configuration.schema import object_of, options_of

SCHEMA = object_of(demosaic=options_of("RCD+VNG4", "LMMSE"))

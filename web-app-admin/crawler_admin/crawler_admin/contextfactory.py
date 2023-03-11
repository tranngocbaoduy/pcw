from scrapy.core.downloader.contextfactory import ScrapyClientContextFactory
from cryptography.hazmat.bindings.openssl.binding import Binding


class LegacyConnectContextFactory(ScrapyClientContextFactory):

    def getContext(self, hostname=None, port=None):
        ctx = self.getCertificateOptions().getContext()
        binding = Binding()
        ctx.set_options(binding.lib.SSL_OP_ALLOW_UNSAFE_LEGACY_RENEGOTIATION)
        return ctx
 
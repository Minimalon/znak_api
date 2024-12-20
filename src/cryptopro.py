#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from base64 import b64encode
from datetime import datetime
from typing import Union
import subprocess

from src.config import certificate_config

sys.path.append('/opt/pycades_0.1.44290/')

if os.name == 'posix':
    import pycades


class CryproPro:
    def __init__(self):
        self.thumbprint = certificate_config.thumbprint
        self.pin = certificate_config.pin
        if os.name == 'posix':
            self.signer = self.get_signer()
        self.cert_info = None

    def parse_detail(self, row):
        if row:
            detail = dict(
                key_val.split('=')
                for key_val in row.split(', ')
            )
            detail['row'] = row
            return detail

    def certificate_info(self, cert=None):
        """Данные сертификата."""
        if cert is None and self.thumbprint is not None:
            cert = self.get_certificate()
        pkey = cert.PrivateKey
        algo = cert.PublicKey().Algorithm

        cert_info = {
            'privateKey': {
                'providerName': pkey.ProviderName,
                'uniqueContainerName': pkey.UniqueContainerName,
                'containerName': pkey.ContainerName,
            },
            'algorithm': {
                'name': algo.FriendlyName,
                'val': algo.Value,
            },
            'valid': {
                'from': cert.ValidFromDate,
                'to': cert.ValidToDate,
            },
            # 'issuer': self.parse_detail(cert.IssuerName),
            'subject': self.parse_detail(cert.SubjectName),
            'thumbprint': cert.Thumbprint,
            'serialNumber': cert.SerialNumber,
            'hasPrivateKey': cert.HasPrivateKey()
        }
        return cert_info

    def get_certificate(self):
        store = pycades.Store()
        store.Open(
            pycades.CAPICOM_CURRENT_USER_STORE,
            pycades.CAPICOM_MY_STORE,
            pycades.CAPICOM_STORE_OPEN_MAXIMUM_ALLOWED
        )
        try:
            certificates = store.Certificates.Find(
                pycades.CAPICOM_CERTIFICATE_FIND_SHA1_HASH,
                self.thumbprint
            )
            if certificates.Count == 0:
                raise ValueError("Сертификат с указанным отпечатком не найден.")
            cert = certificates.Item(1)
            if not cert.HasPrivateKey():
                raise ValueError("Сертификат не содержит закрытого ключа.")
            return cert
        finally:
            store.Close()

    def get_signer(self):
        cert = self.get_certificate()
        signer = pycades.Signer()
        signer.Certificate = cert
        signer.CheckCertificate = True
        signer.KeyPin = self.pin
        return signer

    async def sign_data(self, data):
        signed_data = pycades.SignedData()
        signed_data.ContentEncoding = pycades.CADESCOM_BASE64_TO_BINARY
        signed_data.Content = data
        signature = signed_data.SignCades(
            self.signer,
            pycades.CADESCOM_CADES_BES
        )
        return signature
    # def get_signer(self):
    #     try:
    #         signer = pycades.Signer()
    #         signer.Certificate = self.get_certificate()
    #         signer.CheckCertificate = True
    #         signer.KeyPin = self.pin  # Убедитесь, что PIN-код задан корректно
    #         return signer
    #     except Exception as e:
    #         print(f"Ошибка при получении подписанта: {e}")
    #         raise
    #
    # async def signing_data(self, data):
    #     """
    #     Подпись текста (Для получения токена)
    #     detached - Истина/Ложь - откреплённая(для подписания документов)/прикреплённая(для получения токена авторизации) подпись
    #     """
    #     signed_data = pycades.SignedData()
    #     signed_data.ContentEncoding = pycades.CADESCOM_BASE64_TO_BINARY
    #     signed_data.Content = data
    #     signature = signed_data.SignCades(self.signer, pycades.CADESCOM_CADES_BES)
    #     return signature

    def signing_data_with_user(self, data):
        """
        Подпись текста (Для получения токена)
        detached - Истина/Ложь - откреплённая(для подписания документов)/прикреплённая(для получения токена авторизации) подпись
        """
        signer = pycades.Signer()
        signer.Certificate = self.get_certificate()
        signer.CheckCertificate = True
        signer.KeyPin = self.pin
        signer.Options = pycades.CAPICOM_CERTIFICATE_INCLUDE_CHAIN_EXCEPT_ROOT
        signed_data = pycades.SignedData()
        signed_data.ContentEncoding = pycades.CADESCOM_BASE64_TO_BINARY
        signed_data.Content = data
        signature = signed_data.SignCades(signer, pycades.CADESCOM_CADES_BES)
        return signature

    def signing_pdf(self, data):
        signed_data = pycades.SignedData()
        signed_data.Content = data
        return signed_data.SignCades(self.signer, pycades.CADESCOM_CADES_BES, False, 0)

    def signing_how_in_javascript(self, data, detached=False):
        signed_data = pycades.SignedData()
        signed_data.ContentEncoding = pycades.CADESCOM_BASE64_TO_BINARY
        signed_data.Content = data
        return signed_data.SignCades(self.signer, pycades.CADESCOM_CADES_BES, detached)

    def signing_xml(self, data, encoding='utf-8'):
        """Подпись XML"""
        signedXML = pycades.SignedXML()
        signedXML.Content = data
        signedXML.SignatureType = pycades.CADESCOM_XML_SIGNATURE_TYPE_ENVELOPED | pycades.CADESCOM_XADES_BES
        signature = signedXML.Sign(self.signer)
        return signature

    def signing_hash(self, data: Union[str, bytes, bytearray], encoding="utf-8") -> str:
        """Подпись хэш"""
        if isinstance(data, str):
            data = bytes(data.encode(encoding))

        hashed_data = pycades.HashedData()
        hashed_data.DataEncoding = pycades.CADESCOM_BASE64_TO_BINARY
        hashed_data.Algorithm = (
            pycades.CADESCOM_HASH_ALGORITHM_CP_GOST_3411_2012_256
        )
        hashed_data.Hash(b64encode(data).decode())
        byte_hash = bytes.fromhex(hashed_data.Value)
        return b64encode(byte_hash).decode()

    def read_certificate(self, cert_path):
        with open(cert_path, "rb") as f:
            cert = pycades.Certificate()
            cert.Import(f.read())
        return self.certificate_info(cert)

    def sign_detach_data(self, data: str, file_path: str, encode: str = 'windows-1251') -> str:
        """
        Отсоединённая подпись
        :param data: Данные которые подписывать
        :param file_path: Путь куда сохраним файл подписываем. Также сохраняет подписыванный файл с окончанием .sig
        :param encode: Кодировка
        :return: Подпись в формате base64
        """
        with open(file_path, 'wb') as file:
            file.write(data.encode(encode))

        sign = f"/opt/cprocsp/bin/amd64/csptest -sfsign -sign -add -detached -base64 -in {file_path} -out {file_path}.sig -my '{self.thumbprint}'"
        cat = f'cat {file_path}.sig | tr -d "\n"'
        delete = f'rm {file_path}.sig'
        result_sign = subprocess.run(sign, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result_sign.returncode != 0:
            raise AttributeError(result_sign.stderr)
        result = subprocess.run(cat, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        # subprocess.run(delete, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        return result.stdout

// This file is dual licensed under the terms of the Apache License, Version
// 2.0, and the BSD License. See the LICENSE file in the root of this repository
// for complete details.

use pyo3::conversion::ToPyObject;

enum PyAsn1Error {
    Asn1(asn1::ParseError),
    Py(pyo3::PyErr),
}

impl From<asn1::ParseError> for PyAsn1Error {
    fn from(e: asn1::ParseError) -> PyAsn1Error {
        PyAsn1Error::Asn1(e)
    }
}

impl From<pyo3::PyErr> for PyAsn1Error {
    fn from(e: pyo3::PyErr) -> PyAsn1Error {
        PyAsn1Error::Py(e)
    }
}

impl From<PyAsn1Error> for pyo3::PyErr {
    fn from(e: PyAsn1Error) -> pyo3::PyErr {
        match e {
            PyAsn1Error::Asn1(asn1_error) => pyo3::exceptions::PyValueError::new_err(format!(
                "error parsing asn1 value: {:?}",
                asn1_error
            )),
            PyAsn1Error::Py(py_error) => py_error,
        }
    }
}

#[pyo3::prelude::pyfunction]
fn parse_tls_feature(py: pyo3::Python<'_>, data: &[u8]) -> pyo3::PyResult<pyo3::PyObject> {
    let tls_feature_type_to_enum = py
        .import("cryptography.x509.extensions")?
        .getattr("_TLS_FEATURE_TYPE_TO_ENUM")?;

    let features = asn1::parse::<_, PyAsn1Error, _>(data, |p| {
        let features = pyo3::types::PyList::empty(py);
        for el in p.read_element::<asn1::SequenceOf<u64>>()? {
            let feature = el?;
            let py_feature = tls_feature_type_to_enum.get_item(feature.to_object(py))?;
            features.append(py_feature)?;
        }
        Ok(features)
    })?;

    let x509_module = py.import("cryptography.x509")?;
    x509_module
        .call1("TLSFeature", (features,))
        .map(|o| o.to_object(py))
}

#[pyo3::prelude::pyfunction]
fn parse_precert_poison(py: pyo3::Python<'_>, data: &[u8]) -> pyo3::PyResult<pyo3::PyObject> {
    asn1::parse::<_, PyAsn1Error, _>(data, |p| {
        p.read_element::<()>()?;
        Ok(())
    })?;

    let x509_module = py.import("cryptography.x509")?;
    x509_module.call0("PrecertPoison").map(|o| o.to_object(py))
}

#[pyo3::prelude::pyfunction]
fn parse_spki_for_data(py: pyo3::Python<'_>, data: &[u8]) -> pyo3::PyResult<pyo3::PyObject> {
    let result = asn1::parse::<_, PyAsn1Error, _>(data, |p| {
        p.read_element::<asn1::Sequence>()?
            .parse::<_, PyAsn1Error, _>(|p| {
                // AlgorithmIdentifier
                p.read_element::<asn1::Sequence>()?
                    .parse::<_, PyAsn1Error, _>(|p| {
                        p.read_element::<asn1::ObjectIdentifier>()?;
                        if !p.is_empty() {
                            p.read_element::<asn1::Tlv>()?;
                        }
                        Ok(())
                    })?;

                let pubkey_data = p.read_element::<asn1::BitString>()?;
                if pubkey_data.padding_bits() != 0 {
                    return Err(pyo3::exceptions::PyValueError::new_err(
                        "Invalid public key encoding",
                    )
                    .into());
                }
                Ok(pubkey_data.as_bytes())
            })
    })?;

    Ok(pyo3::types::PyBytes::new(py, result).to_object(py))
}

pub(crate) fn create_submodule(py: pyo3::Python) -> pyo3::PyResult<&pyo3::prelude::PyModule> {
    let submod = pyo3::prelude::PyModule::new(py, "asn1")?;
    submod.add_wrapped(pyo3::wrap_pyfunction!(parse_tls_feature))?;
    submod.add_wrapped(pyo3::wrap_pyfunction!(parse_precert_poison))?;
    submod.add_wrapped(pyo3::wrap_pyfunction!(parse_spki_for_data))?;

    Ok(submod)
}

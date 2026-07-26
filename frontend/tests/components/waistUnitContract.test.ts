/**
 * Waist explicit-unit payload helpers used by QuestionnaireForm.
 */

import {
  WAIST_CM_DICT_KEY,
  WAIST_EXPLICIT_UNIT_CONTRACT,
  WAIST_INCHES_DICT_KEY,
} from '@/components/forms/QuestionnaireForm'

describe('waist unit contract constants', () => {
  it('exports stable SSOT dictionary keys and contract stamp', () => {
    expect(WAIST_CM_DICT_KEY).toBe('Waist circumference (cm)')
    expect(WAIST_INCHES_DICT_KEY).toBe('Waist circumference (inches)')
    expect(WAIST_EXPLICIT_UNIT_CONTRACT).toBe('waist_explicit_unit_v1')
  })

  it('cm payload shape matches backend contract', () => {
    const payload = {
      waist_circumference: { [WAIST_CM_DICT_KEY]: 166 },
      _questionnaire_contract: {
        version: WAIST_EXPLICIT_UNIT_CONTRACT,
        waist_unit: 'explicit_v1',
      },
    }
    expect(payload.waist_circumference[WAIST_CM_DICT_KEY]).toBe(166)
    expect(payload._questionnaire_contract.version).toBe(WAIST_EXPLICIT_UNIT_CONTRACT)
  })

  it('inches payload shape matches backend contract', () => {
    const payload = {
      waist_circumference: { [WAIST_INCHES_DICT_KEY]: 36 },
      _questionnaire_contract: { version: WAIST_EXPLICIT_UNIT_CONTRACT },
    }
    expect(payload.waist_circumference[WAIST_INCHES_DICT_KEY]).toBe(36)
  })
})

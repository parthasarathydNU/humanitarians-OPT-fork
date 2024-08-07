-- WORKSPACES

UPDATE workspaces
SET default_model = 'gpt-4-turbo-preview'
WHERE default_model = 'gpt-4-1106-preview';

UPDATE workspaces
SET default_model = 'gpt-3.5-turbo'
WHERE default_model = 'gpt-3.5-turbo-1106';

-- PRESETS

UPDATE presets
SET model = 'gpt-4-turbo-preview'
WHERE model = 'gpt-4-1106-preview';

UPDATE presets
SET model = 'gpt-3.5-turbo'
WHERE model = 'gpt-3.5-turbo-1106';

-- ASSISTANTS

UPDATE assistants
SET model = 'gpt-4-turbo-preview'
WHERE model = 'gpt-4-1106-preview';

UPDATE assistants
SET model = 'gpt-3.5-turbo'
WHERE model = 'gpt-3.5-turbo-1106';

-- CHATS

UPDATE chats
SET model = 'gpt-4-turbo-preview'
WHERE model = 'gpt-4-1106-preview';

UPDATE chats
SET model = 'gpt-3.5-turbo'
WHERE model = 'gpt-3.5-turbo-1106';

-- MESSAGES

UPDATE messages
SET model = 'gpt-4-turbo-preview'
WHERE model = 'gpt-4-1106-preview';

UPDATE messages
SET model = 'gpt-3.5-turbo'
WHERE model = 'gpt-3.5-turbo-1106';

-- PROFILES

CREATE OR REPLACE FUNCTION create_profile_and_workspace() 
RETURNS TRIGGER
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
DECLARE
    random_username TEXT;
BEGIN
    -- Generate a random username
    random_username := 'user' || substr(replace(gen_random_uuid()::text, '-', ''), 1, 16);

    -- Create a profile for the new user
    INSERT INTO public.profiles(user_id, anthropic_api_key, azure_openai_35_turbo_id, azure_openai_45_turbo_id, azure_openai_45_vision_id, azure_openai_api_key, azure_openai_endpoint, google_gemini_api_key, has_onboarded, image_url, image_path, mistral_api_key, display_name, bio, openai_api_key, openai_organization_id, perplexity_api_key, profile_context, use_azure_openai, username)
    VALUES(
        NEW.id,
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        FALSE,
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        FALSE,
        random_username
    );

    INSERT INTO public.workspaces(user_id, is_home, name, default_context_length, default_model, default_prompt, default_temperature, description, embeddings_provider, include_profile_context, include_workspace_instructions, instructions, bot_type)
    VALUES(
        NEW.id,
        TRUE,
        'Home',
        4096,
        'gpt-4-turbo-preview', -- Updated default model
        'You are an expert in rubric generation for any given type of assignment. Once a user submits an assignment, use the flipped interaction pattern to ask the user questions about their grading preferences, which areas of the assignment that they want greater emphasis on. The conversation should be engaging to the user. The questions can be regarding: Their style of grading , how strict do they want to be and other questions to arrive at a well defined and clear grading schema without any ambiguity. Further ask questions regarding the user to understand more about their personal as well. Finally based on the gathered preferences, use the persona pattern to take the persona of the user and generate a rubric that matches their style. Start by greeting the user and ask one question at a time. Ask the first question about what is the type of assignment they want help with.',
        0.5,
        'My home workspace for Rubric Generation.',
        'openai',
        TRUE,
        TRUE,
        '',
        'Rubric'
    );

    -- Create the home workspace for the new user
    INSERT INTO public.workspaces(user_id, is_home, name, default_context_length, default_model, default_prompt, default_temperature, description, embeddings_provider, include_profile_context, include_workspace_instructions, instructions, bot_type)
    VALUES(
          NEW.id,
          FALSE,
          'Home',
          4096,
          'gpt-4-turbo-preview',
          'You are an expert in assignment generation for any given course topic. Once a user submits a course topic, use the flipped interaction pattern to ask the user questions about their assignment preferences, which sub-topic of the given topic that they want greater emphasis on. The conversation should be engaging to the user. The questions can be regarding: How many questions they want to include in the assignment , what type of questions the user want to include in the assignment (MCQs, brief, essay writing etc.), what is the difficulty of the assignment that they are looking for to arrive at a well defined assignment. Further ask questions regarding the user to understand more about their personal as well. Finally based on the gathered preferences, use the persona pattern to take the persona of the user and generate a assignment that matches their style. Start by greeting the user and ask one question at a time. Ask the first question about what is the topic for assignment generation that they want help with.',
          0.5,
          'My home workspace for Assignment Generation.',
          'openai',
          TRUE,
          TRUE,
          '',
          'Assignment'
      );

    RETURN NEW;
END;
$$;
